import os
import shutil
from audcon import log, app
from audcon.models import *
from audcon.modules import functions, enqueue


def convert():
    log.info('converter starting')
    # Find the last run log entry
    last_run_log = RunLog.query.filter_by(service='converter').order_by(RunLog.created_date.desc()).first()

    if last_run_log is not None:
        if last_run_log.status == 'running' and last_run_log.last_ran() < 86400:
            log.error('already running since {}'.format(last_run_log.created_date_local_tz()))
            return True

    # Add new RunLog entry
    log.debug('creating runlog entry')
    run_log_entry = RunLog(service='converter', status='running')
    db.session.add(run_log_entry)
    db.session.commit()

    # Get the ID
    db.session.refresh(run_log_entry)
    log.debug('runlog entry: {}'.format(str(run_log_entry.id)))

    # Start processing
    queue = Queue.query.filter_by(media_converted=False).order_by(Queue.id).all()
    converted_count = 0

    if queue is not None:
        log.info('queue size: {}'.format(len(queue)))

        for item in queue:
            temp_file = os.path.join(app.config['TEMP_FOLDER'], os.path.basename(item.media_output_file_path))
            log.info('input file: {}'.format(item.media_file_path))
            log.info('output file: {}'.format(item.media_output_file_path))
            log.info('params: {}'.format(item.media_output_ffmpeg_params))

            try:
                ffmpeg_success, ffmpeg = functions.ffmpeg(input_file=item.media_file_path,
                                                          output_file=temp_file, params=item.media_output_ffmpeg_params)
                log.debug('ffmpeg output ' + ffmpeg)
            except Exception as e:
                log.error('error occcurred running ffmpeg')
                log.error(e)
            else:
                if ffmpeg_success:
                    log.info('conversion done')
                    converted_count = converted_count + 1

                    if app.config['REMOVE_SRC_FILE']:
                        # Remove original file
                        log.info('removing input file')
                        try:
                            os.remove(item.media_file_path)
                        except IOError as e:
                            log.warning('could not remove input file')
                            log.warning(e)
                        else:
                            log.info('input file removed')

                    log.info('moving converted file to final location')
                    try:
                        output_folder = os.path.dirname(item.media_output_file_path)
                        if not os.path.exists(output_folder):
                            log.info('output folder {} does not exist, creating it'.format(output_folder))
                            if os.mkdir(output_folder):
                                log.info('output folder created')
                            else:
                                log.error('could not create output folder')

                        shutil.move(temp_file, item.media_output_file_path)
                    except IOError as e:
                        log.error('could not move to destination ')
                        log.error(e)
                    else:
                        log.info('successfully moved')
                        log.info('updating queue')

                        item.media_converted = True
                        db.session.commit()
                        db.session.refresh(item)

                        if item.media_converted:
                            log.info('queue updated')
                        else:
                            log.error('error updating queue')

                else:
                    log.error('error running ffmpeg')

    else:
        log.info('queue empty')

    # Update RunLog
    params = {
        'queue_size': len(queue),
        'converted_count': converted_count
    }

    run_log_entry.status='complete'
    run_log_entry.params = params
    db.session.commit()


