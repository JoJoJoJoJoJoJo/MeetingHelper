import os


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'You Shall Not Pass'
    UPLOAD_PATH_BASE = 'http://raasr.xfyun.cn/api'
    API_APP_ID = '5f00a689'
    API_SECRET_KEY = '48d43463208dc202f6590636c74c7b6a'
    FILE_PIECE_SIZE = 10485760
