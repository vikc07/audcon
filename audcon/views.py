import math
from flask import render_template, flash, redirect, url_for, request
from audcon.forms import *
from audcon.models import *
from audcon.modules import functions, scanner, converter
from audcon import configuration


@app.route('/')
@app.route('/index')
@app.route('/index/p/<int:page>')
def index(page=1):
    title = 'Media'
    page_limit = app.config['UI']['ITEMS_PER_PAGE']

    if functions.sha256(configuration.CFG_FILE_PATH) == functions.sha256(configuration.DEFAULT_CFG_FILE_PATH):
        return redirect(url_for('settings'))
    else:
        records = Media.query.filter_by(isdeleted=False).limit(page_limit).offset((page - 1) * page_limit).all()
        pages = math.ceil(Media.query.filter_by(isdeleted=False).count() / page_limit)
        return render_template('index.html', records=records, title=title, pages=pages, current_page=page)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    title = 'Settings'
    form = CoreConfigurationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            configuration.cfg.DB['HOST'] = request.form.get('dbhost')
            configuration.cfg.DB['PORT'] = int(request.form.get('dbport'))
            configuration.cfg.DB['NAME'] = request.form.get('dbname')
            configuration.cfg.DB['USER'] = request.form.get('dbuser')
            configuration.cfg.DB['PASS'] = request.form.get('dbpass')

            if request.form.get('alerts_enabled'):
                configuration.cfg.ALERTS['ENABLED'] = True
                configuration.cfg.ALERTS['FROM_ADDRESS'] = request.form.get('alerts_from_address')
                configuration.cfg.ALERTS['TO_ADDRESS'] = request.form.get('alerts_to_address')
                configuration.cfg.ALERTS['SMTP_HOST'] = request.form.get('alerts_smtp_host')
                configuration.cfg.ALERTS['SMTP_PORT'] = int(request.form.get('alerts_smtp_port'))
                configuration.cfg.ALERTS['SMTP_USER'] = request.form.get('alerts_smtp_user')
                configuration.cfg.ALERTS['SMTP_PASS'] = request.form.get('alerts_smtp_pass')
                if request.form.get('alerts_smtp_tls'):
                    configuration.cfg.ALERTS['SMTP_TLS_ENABLED'] = True
                else:
                    configuration.cfg.ALERTS['SMTP_TLS_ENABLED'] = False
            else:
                configuration.cfg.ALERTS['ENABLED'] = False
                configuration.cfg.ALERTS['FROM_ADDRESS'] = None
                configuration.cfg.ALERTS['TO_ADDRESS'] = None
                configuration.cfg.ALERTS['SMTP_HOST'] = None
                configuration.cfg.ALERTS['SMTP_PORT'] = None
                configuration.cfg.ALERTS['SMTP_USER'] = None
                configuration.cfg.ALERTS['SMTP_PASS'] = None
                configuration.cfg.ALERTS['SMTP_TLS_ENABLED'] = False

            configuration.cfg.MEDIA_FOLDER[0] = request.form.get('media_folder')
            if request.form.get('media_scan_recursively'):
                configuration.cfg.MEDIA_SCAN_RECURSIVELY = True
            else:
                configuration.cfg.MEDIA_SCAN_RECURSIVELY = False

            configuration.cfg.UI['ITEMS_PER_PAGE'] = int(request.form.get('ui_items_per_page'))
            configuration.cfg.UI['TZ'] = request.form.get('ui_time_zone')

            configuration.save_config()
            configuration.reload_config()

            flash('Settings have been saved')
        else:
            flash('Error')
        return redirect(url_for('settings'))
    else:
        form.dbhost.data = app.config['DB']['HOST']
        form.dbport.data = app.config['DB']['PORT']
        form.dbname.data = app.config['DB']['NAME']
        form.dbuser.data = app.config['DB']['USER']
        form.dbpass.data = app.config['DB']['PASS']
        form.alerts_enabled.data = app.config['ALERTS']['ENABLED']
        form.alerts_from_address.data = app.config['ALERTS']['FROM_ADDRESS']
        form.alerts_to_address.data = app.config['ALERTS']['TO_ADDRESS']
        form.alerts_smtp_host.data = app.config['ALERTS']['SMTP_HOST']
        form.alerts_smtp_port.data = app.config['ALERTS']['SMTP_PORT']
        form.alerts_smtp_user.data = app.config['ALERTS']['SMTP_USER']
        form.alerts_smtp_pass.data = app.config['ALERTS']['SMTP_PASS']
        form.alerts_smtp_tls.data = app.config['ALERTS']['SMTP_TLS_ENABLED']
        form.media_folder.data = app.config['MEDIA_FOLDER'][0]
        form.media_scan_recursively.data = app.config['MEDIA_SCAN_RECURSIVELY']
        form.ui_items_per_page.data = app.config['UI']['ITEMS_PER_PAGE']
        form.ui_time_zone.data = app.config['UI']['TZ']

        return render_template('settings.html', title=title, form=form)


@app.route('/scan')
def scan():
    scanner.scan()
    return redirect(url_for('index'))


@app.route('/scan/full')
def scan_full():
    scanner.scan(full_scan=True)
    return redirect(url_for('index'))


@app.route('/queue')
@app.route('/queue/p/<int:page>')
def queue(page=1):
    title = 'Queue'
    page_limit = app.config['UI']['ITEMS_PER_PAGE']

    records = Queue.query.filter_by(isdeleted=False).order_by(Queue.id.desc()).limit(page_limit).offset((page - 1) *
                                                                                           page_limit).all()
    pages = math.ceil(Queue.query.count() / page_limit)
    return render_template('queue.html', records=records, title=title, pages=pages, current_page=page)


@app.route('/converter')
def convert():
    converter.convert()
    return redirect(url_for('queue'))


@app.route('/activity')
@app.route('/activity/p/<int:page>')
def activity(page=1):
    title = 'Activity'
    page_limit = app.config['UI']['ITEMS_PER_PAGE']

    records = RunLog.query.order_by(RunLog.id.desc()).limit(page_limit).offset((page - 1) * page_limit).all()
    pages = math.ceil(RunLog.query.count() / page_limit)
    return render_template('activity.html', records=records, title=title, pages=pages, current_page=page)
