from . import app, db
from .forms import FileForm
from . models import SubmitRecord
from api import RequestApi
from word_generator import WordGenerator

from flask import flash, request, render_template, send_file, make_response

import json

SUCCESS_STATE = '识别完成'
IN_PROGRESS_STATE = '任务创建成功'
FAIL_STATE = '失败'


#  views
@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        api = RequestApi(file)
        record = SubmitRecord.query.filter_by(file_hash=api.file_hash).first()
        if record and record.state != FAIL_STATE:
            flash('文件已经识别过了哦～，可以在下面的列表里找到。文件名：{}'.format(record.file_name))
        else:
            if record:
                db.session.delete(record)
            api.call()
            record = SubmitRecord(file_hash=api.file_hash, task_id=api.task_id, file_name=api.file_name, state='上传成功')
            db.session.add(record)
            db.session.commit()
            flash('上传成功，请稍候哦~')
    records = SubmitRecord.query.all()
    return render_template('index.html', form=form, records=records)


@app.route('/progress', methods=['POST'])
def get_progress():
    task_id = request.form['task_id']
    record = SubmitRecord.query.filter_by(task_id=task_id).first()
    if record.state == SUCCESS_STATE:
        return record.state
    result = RequestApi.get_progress(task_id)
    state = IN_PROGRESS_STATE
    if result['err_no'] != 0 and result['err_no'] != 26605:
        record.error_no = result['err_no']
        record.error = result['failed']
        state = FAIL_STATE
        record.state = state
        db.session.add(record)
        db.session.commit()
    else:
        status = json.loads(result['data'])
        if status['status'] == 9:
            state = SUCCESS_STATE
            record.state = state
            db.session.add(record)
            db.session.commit()
    return state


@app.route('/result', methods=['POST'])
def get_result():
    task_id = request.form['task_id']
    record = SubmitRecord.query.filter_by(task_id=task_id).first()
    if record.result:
        return record.state
    result = RequestApi.get_result(task_id)
    if result['err_no'] != 0:
        record.error_no = result['err_no']
        record.error = result['failed']
        state = FAIL_STATE
        record.state = state
        db.session.add(record)
        db.session.commit()
        return state
    else:
        record.result = result['data']
        state = SUCCESS_STATE
        record.state = state
        db.session.add(record)
        db.session.commit()
    return state


@app.route('/word', methods=['POST'])
def get_word():
    task_id = request.form['task_id']
    show_details = request.form['show_details'] == 'true'
    record = SubmitRecord.query.filter_by(task_id=task_id).first()
    data = json.loads(record.result)
    generator = WordGenerator(record.file_name, data, show_details)
    generator.generate()
    filename = generator.filename
    return filename


@app.route('/file/<filename>')
def getfile(filename):
    response = make_response(send_file(WordGenerator.get_file_path(filename)))
    response.headers['Content-Disposition'] = 'attachment;filename={};'.format(filename).encode('utf-8')
    return response
