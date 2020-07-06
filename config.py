import os


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'You Shall Not Pass'
    BOOTSTRAP_SERVE_LOCAL = True
    UPLOAD_PATH_BASE = 'http://raasr.xfyun.cn/api'
    API_APP_ID = os.environ.get('XF_APP_ID')
    API_SECRET_KEY = os.environ.get('XF_SECRET_KEY')
    FILE_PIECE_SIZE = 10485760
