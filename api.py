from config import Config

import time
import hmac
import hashlib
import base64
import requests
import json


class SliceIdGenerator:
    def __init__(self, base='slice'):
        self.base = base
        self.start = 0

    def get_next_id(self):
        self.start += 1
        return self.base + str(self.start)


class RequestApi:
    def __init__(self, file):
        self.app_id = Config.API_APP_ID
        self.secret_key = Config.API_SECRET_KEY
        self.file = file
        self.file_name = file.filename
        self.file_len = 0
        self.file_hash = ''
        self.task_id = 0
        self.file_slices = {}
        self.slice_num = 0
        self.handle_file()

    @classmethod
    def get_common_params(cls):
        app_id = Config.API_APP_ID
        secret_key = Config.API_SECRET_KEY
        ts = str(int(time.time()))
        md5 = hashlib.md5()
        md5.update((app_id + ts).encode('utf-8'))
        md = bytes(md5.hexdigest(), encoding='utf-8')
        signa = hmac.new(secret_key.encode('utf-8'), md, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return {
            'app_id': app_id,
            'signa': signa,
            'ts': ts,
        }

    @staticmethod
    def post(api_name, data, files=None, headers=None):
        url = Config.UPLOAD_PATH_BASE + api_name
        response = requests.post(url, data, files=files, headers=headers)
        result = json.loads(response.text)
        if result["ok"] == 0:
            print("{} success:".format(api_name) + str(result))
        else:
            print("{} error:".format(api_name) + str(result))
        return result

    def handle_file(self):
        file_piece_size = Config.FILE_PIECE_SIZE
        sig = SliceIdGenerator()
        md5 = hashlib.md5()

        while True:
            content = self.file.read(file_piece_size)
            if not content or len(content) == 0:
                break
            self.slice_num += 1
            self.file_len += len(content)
            self.file_slices[sig.get_next_id()] = content
            md5.update(content)
        self.file_hash = md5.hexdigest()

    def prepare(self):
        params = self.get_common_params()
        params['file_len'] = self.file_len
        params['file_name'] = self.file_name
        params['slice_num'] = self.slice_num
        result = self.post('/prepare', params)
        self.task_id = result['data']

    def upload(self):
        params = self.get_common_params()
        params['task_id'] = self.task_id
        for slice_id, content in self.file_slices:
            param = params.copy()
            param['slice_id'] = slice_id
            self.post('/upload', param, files={'filename': slice_id, 'content': content})

    def merge(self):
        params = self.get_common_params()
        params['file_name'] = self.file_name
        params['task_id'] = self.task_id
        self.post('/merge', params)

    @classmethod
    def get_progress(cls,task_id):
        params = cls.get_common_params()
        params['task_id'] = task_id
        cls.post('/getProgress', params)

    @classmethod
    def get_result(cls, task_id):
        params = cls.get_common_params()
        params['task_id'] = task_id
        cls.post('/getResult', params)

    def call(self):
        self.prepare()
        self.upload()
        self.merge()
