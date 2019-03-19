from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
from audcon.modules import functions


class CoreConfigurationForm(FlaskForm):
    # Database
    dbhost = StringField('Host', validators=[DataRequired()])
    dbport = IntegerField('Port', validators=[DataRequired(), NumberRange(min=1, max=65535)])
    dbname = StringField('Database', validators=[DataRequired()])
    dbuser = StringField('User', validators=[DataRequired()])
    dbpass = StringField('Password', validators=[DataRequired()])

    # Email
    alerts_enabled = BooleanField('Alerts Enabled')
    alerts_from_address = StringField('From Email')
    alerts_to_address = StringField('Recipient Email')
    alerts_smtp_host = StringField('SMTP Host')
    alerts_smtp_port = IntegerField('SMTP Port', validators=[NumberRange(min=1, max=65535)])
    alerts_smtp_tls = BooleanField('Enable TLS')
    alerts_smtp_user = StringField('SMTP User')
    alerts_smtp_pass = StringField('SMTP Password')

    # Media
    media_folder = StringField('Folder', validators=[DataRequired()])
    media_scan_recursively = BooleanField('Scan Recursively')

    # UI
    ui_items_per_page = IntegerField('Items per page')
    ui_time_zone = SelectField('Timezone', choices=functions.timezones())

    save = SubmitField('Save')

