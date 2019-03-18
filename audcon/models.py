from datetime import datetime
import pytz
from audcon import db
from gpm import formatting
from audcon import app


class DefaultColumns(object):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    isdeleted = db.Column(db.Integer, default=False)

    def created_date_local_tz(self):
        utc = pytz.timezone('UTC')
        local_tz = pytz.timezone(app.config['UI']['TZ'])
        created_date_utc = utc.localize(self.created_date)
        created_date_local_tz = created_date_utc.astimezone(local_tz)

        return created_date_local_tz.replace(tzinfo=None)

    def modified_date_local_tz(self):
        utc = pytz.timezone('UTC')
        local_tz = pytz.timezone(app.config['UI']['TZ'])
        modified_date_utc = utc.localize(self.modified_date)
        modified_date_local_tz = modified_date_utc.astimezone(local_tz)

        return modified_date_local_tz.replace(tzinfo=None)

    def duration(self):
        return (self.modified_date - self.created_date).total_seconds()

    def duration_formatted(self):
        return formatting.time_pretty((self.modified_date - self.created_date).total_seconds())


class Media(DefaultColumns, db.Model):
    media_file_path = db.Column(db.String(255), nullable=False)
    media_title = db.Column(db.String(255), nullable=False)
    media_fsize = db.Column(db.BigInteger, nullable=False)
    media_format = db.Column(db.String(255), nullable=False)
    media_streams_count = db.Column(db.SmallInteger, nullable=False)
    media_a_streams_count = db.Column(db.SmallInteger, nullable=False)
    media_v_streams_count = db.Column(db.SmallInteger, nullable=False)
    media_s_streams_count = db.Column(db.SmallInteger, nullable=False)
    media_o_streams_count = db.Column(db.SmallInteger, nullable=False)
    media_a_codec = db.Column(db.String(255), nullable=False)
    media_a_sample_fmt = db.Column(db.String(255), nullable=False)
    media_a_sample_rate = db.Column(db.String(255), nullable=False)
    media_a_channels = db.Column(db.String(255), nullable=False)
    media_a_channel_layout = db.Column(db.String(255), nullable=False)
    media_a_bitrate = db.Column(db.String(255), nullable=False)
    media_full_meta = db.Column(db.JSON)

    def __repr__(self):
        return self.media_file_path

    def fsize_pretty(self):
        return formatting.fsize_pretty(self.media_fsize)

    def last_updated(self, formatted=False):
        last_updated = (datetime.utcnow() - self.modified_date).total_seconds()
        if last_updated < 0:
            last_updated = 0

        if formatted:
            return formatting.time_pretty(last_updated)
        return last_updated


class RunLog(DefaultColumns, db.Model):
    service = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255))
    params = db.Column(db.JSON)

    def last_ran(self):
        return (datetime.utcnow() - self.modified_date).total_seconds()


class Queue(DefaultColumns, db.Model):
    media_file_path = db.Column(db.String(255), nullable=False)
    media_output_file_path = db.Column(db.String(255), nullable=False)
    media_output_ffmpeg_params = db.Column(db.String(255), nullable=False)
    media_converted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return self.id

    def conversion_status(self):
        if self.media_converted:
            return 'Complete'
        else:
            return 'Pending'

