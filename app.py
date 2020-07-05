from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import FileForm
from config import Config
from api import RequestApi

import json

app = Flask(__name__)
app.config.from_object(Config)
bp = Bootstrap()
bp.init_app(app)


def upload(file, filename):
    params = api.get_common_params()
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    task_id = ''
    progress = ''
    filename = ''
    # if form.validate_on_submit():
    if form.is_submitted():  # fixme
        file = form.file.data
        api = RequestApi(file)
        # api.call()
        filename = api.file_name
        progress = '上传成功，转换中'
        task_id = api.task_id
        flash('上传成功，请稍候哦~')
    return render_template('index.html', task_id=task_id, form=form, progress=progress, filename=filename)


@app.route('/progress', methods=['POST'])
def get_progress():
    data = json.loads(request.get_data())
    task_id = data['task_id']
    result = RequestApi.get_progress(task_id)
    if result['err_no'] != 0 and result['err_no'] != 26605:
        print('task error: ' + result['failed'])
        return 'fail'
    else:
        status = json.loads(result['data'])
        if status['status'] == 9:
            return 'success'
    return 'in_progress'


if __name__ == '__main__':
    app.run(debug=True)

