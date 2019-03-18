import os
import atexit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from audcon import configuration
from gpm import logging


app = Flask(__name__)
app.config.from_object(configuration.cfg)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
log = logging.Log(script=os.path.join(os.path.dirname(os.path.abspath(__file__)),'audcon.py'), log_level=10,
                  rotating=True)
log.info('init')

from audcon import views, models

# Schedule scanner and converter
from apscheduler.schedulers.background import BackgroundScheduler
from audcon.modules import scanner, converter

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scanner.scan, trigger="interval", minutes=15)
scheduler.add_job(converter.convert, trigger="interval", minutes=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
