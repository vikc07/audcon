import os
import time
import json
from audcon import log
from audcon.models import *
from audcon.modules import functions, enqueue
from gpm import formatting


def scan(full_scan = False):
    # Find the last run log entry
    last_run_log = RunLog.query.filter_by(service='scanner').order_by(RunLog.created_date.desc()).first()

    if last_run_log is not None:
        if last_run_log.status == 'running' and last_run_log.last_ran() < 86400:
            log.error('already running since {}'.format(last_run_log.created_date_local_tz()))
            return True

    # Add new RunLog entry
    log.debug('creating runlog entry')
    run_log_entry = RunLog(service='scanner', status='running')
    db.session.add(run_log_entry)
    db.session.commit()

    # Get the ID
    db.session.refresh(run_log_entry)
    log.debug('runlog entry: {}'.format(str(run_log_entry.id)))

    # Start processing
    log.info('fetching all files')
    all_files = functions.get_files(folders=app.config['MEDIA_FOLDER'], recursive=app.config['MEDIA_SCAN_RECURSIVELY'])

    # Find all files that have been created or modified since last run
    if last_run_log is not None and not full_scan:
        last_ran_in_s = last_run_log.last_ran()
        log.debug('last ran {}'.format(formatting.time_pretty(last_ran_in_s)))
    else:
        last_ran_in_s = -1
        log.warning('first time running, could take longer')

    files_to_scan = []
    for file in all_files:
        log.debug('file: {}'.format(file))
        # Skip os files e.g. ._
        if os.path.basename(file).startswith('._'):
            log.debug('skipping file: {}'.format(file))
        elif os.path.exists(file):
            # Find extension and file size
            ext = functions.get_file_extension(file)
            if ext in app.config['FILE_TYPES']: # Check if file exists
                log.info(ext.strip('.') + ': ' + file)

                file_last_updated_in_s = (time.time() - os.path.getmtime(file))
                if last_ran_in_s > file_last_updated_in_s or last_ran_in_s == -1:
                    log.debug('file: {}'.format(file))
                    log.debug('file_last_updated_in_s: {}'.format(formatting.time_pretty(file_last_updated_in_s)))

                    # Find extension and file size
                    ext = functions.get_file_extension(file)
                    if ext in app.config['FILE_TYPES']:
                        log.info(ext.strip('.') + ': ' + file)
                        log.debug('adding to scan list')
                        files_to_scan.append(file)
                else:
                    log.debug('skipping as metadata has been recently updated: {}'.format(file))
            else:
                log.debug('skipped unsupported file type {}'.format(file))
        else:
            log.debug('skipping as file does not exist: {}'.format(file))

    log.info('{} files to scan'.format(len(files_to_scan)))

    # Now process this shortened list and update db
    for file in files_to_scan:
        log.info('file: {}'.format(file))

        try:
            ffprobe_success, ffprobe_output = functions.ffprobe(file)
            log.debug('ffprobe output {}'.format(ffprobe_output))
        except Exception as e:
            log.error('error occcurred running ffprobe')
            log.error(e)
        else:
            if ffprobe_success:
                file_meta = json.loads(ffprobe_output)
                log.info('format: {}'.format(file_meta.get('format').get('format_name')))

                # Check if we have this file in our database and find out if update/insert
                operation = 'update'
                record = Media.query.filter_by(media_file_path=file).first()
                if record is None:
                    record = Media()
                    record.media_file_path = file
                    operation = 'insert'

                record.media_fsize = os.stat(file).st_size
                record.media_format = file_meta.get('format').get('format_name')

                # Set media title from Tag if available, if not use the file name
                record.media_title = file_meta.get('format').get('tags').get('TITLE')
                if record.media_title is None:
                    record.media_title = functions.get_file_name_without_extension(file)

                # Find number of streams and acodec details
                record.media_streams_count = len(file_meta.get('streams'))
                record.media_a_streams_count = 0
                record.media_v_streams_count = 0
                record.media_s_streams_count = 0
                record.media_o_streams_count = 0
                record.media_a_codec = None
                record.media_a_sample_fmt = None
                record.media_a_sample_rate = None
                record.media_a_channels = None
                record.media_a_channel_layout = None
                record.media_a_bitrate = None
                record.media_full_meta = ffprobe_output

                for stream in file_meta.get('streams'):
                    stream_type = stream.get('codec_type')
                    if stream_type == 'audio':
                        record.media_a_codec = stream.get('codec_name')
                        record.media_a_streams_count += 1

                        # Get only for first stream
                        if record.media_a_streams_count == 1:
                            log.debug('extracting acodec attributes')
                            record.media_a_sample_fmt = stream.get('sample_fmt')
                            record.media_a_sample_rate = stream.get('sample_rate')
                            record.media_a_channels = stream.get('channels')
                            record.media_a_channel_layout = stream.get('channel_layout')
                            record.media_a_bitrate = stream.get('bit_rate')

                            # If bitrate is not there in the stream, get it from upper level format tag
                            if stream.get('bit_rate') is None:
                                record.media_a_bitrate = file_meta.get('format').get('bit_rate')
                        else:
                            log.warning('ignoring this stream: {}'.format(file.get('media_file_path')))
                    elif stream_type == 'video':
                        log.debug('video stream found: {}'.format(file))
                        record.media_v_streams_count += 1
                    elif stream_type == 'subtitle':
                        log.debug('subtitle stream found: {}'.format(file))
                        record.media_s_streams_count += 1
                    else:
                        log.debug('other stream found: {}'.format(file))
                        record.media_o_streams_count += 1

                # Update database
                if operation == 'insert':
                    db.session.add(record)

                db.session.commit()
                db.session.refresh(record)

                # Enqueue
                not_supported = ''
                if record.media_a_codec not in app.config['OK_A_FORMATS']:
                    not_supported = '**not supported'
                    enqueue.enqueue(file)

                log.info('codec: {} {}'.format(record.media_a_codec, not_supported))
            else:
                log.error('error occurred while running ffprobe')

    # Remove dead entries
    log.info('checking for dead entries')
    media = Media.query.filter_by(isdeleted=False).all()
    dead_entries = 0
    for file in media:
        if not os.path.exists(file.media_file_path):
            file.isdeleted = True
            dead_entries += 1

    log.info('found {} dead entries'.format(dead_entries))
    db.session.commit()

    # Update RunLog
    params = {
        'files_scanned': len(files_to_scan),
        'full_scan': full_scan,
        'dead_entries': dead_entries
    }

    run_log_entry.status='complete'
    run_log_entry.params = params
    db.session.commit()



