import os
from audcon import log
from audcon.models import *
from audcon.modules import functions


def enqueue(media_file_path):
    # Find out if this file is already in queue
    record = Queue.query.filter_by(media_file_path=media_file_path, media_converted=False).order_by(
        Queue.modified_date.desc()).first()

    if record is None:
        record = Queue()
        output_folder = functions.get_file_path(media_file_path)
        output_file = os.path.join(output_folder, functions.get_file_name_without_extension(media_file_path) +
                                   app.config['DEFAULT_EXT'])

        record.media_file_path = media_file_path
        record.media_output_file_path = output_file
        record.media_output_ffmpeg_params = app.config['DEFAULT_ACODEC'] + ' ' + app.config['DEFAULT_OPTIONS']

        db.session.add(record)
        db.session.commit()
    else:
        log.debug('file already in queue id: {}'.format(record.id))
