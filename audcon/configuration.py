import os
import shutil
import json
from audcon import app
from gpm import config

cfg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg')
cfg_file = 'config.json'
default_cfg_file = 'default.json'

cfg_file_path = os.path.join(cfg_dir, cfg_file)
default_cfg_file_path = os.path.join(cfg_dir, 'default.json')

if not os.path.exists(cfg_file_path):
    shutil.copy(default_cfg_file_path, cfg_file_path)

cfg = config.Config(script=__file__, cfg_dir=cfg_dir, cfg_file=cfg_file)
cfg.read()


def dburi():
    uri = "{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    cfg.SQLALCHEMY_DATABASE_URI = uri.format(
        DB_TYPE=cfg.DB['TYPE'],
        DB_DRIVER=cfg.DB['DRIVER'],
        DB_USER=cfg.DB['USER'],
        DB_PASS=cfg.DB['PASS'],
        DB_HOST=cfg.DB['HOST'],
        DB_PORT=cfg.DB['PORT'],
        DB_NAME=cfg.DB['NAME']
    )


dburi()
CFG_FILE_PATH = cfg_file_path
DEFAULT_CFG_FILE_PATH = default_cfg_file_path


def save_config():
    dburi()
    with open(CFG_FILE_PATH, 'w') as outfile:
        json.dump(cfg.__dict__, indent=4, fp=outfile)


def reload_config():
    cfg.read()
    app.config.from_object(cfg)
