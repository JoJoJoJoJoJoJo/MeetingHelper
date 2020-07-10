from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import FileForm
from config import Config
from api import RequestApi

import json
import click

app = Flask(__name__)
app.config.from_object(Config)
bp = Bootstrap()
bp.init_app(app)
db = SQLAlchemy()
db.init_app(app)


#  cli
@app.cli.command('initdb')
@click.option('--drop', is_flag=True, help='Drop all then create.')
def initdb(drop=False):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('DB Initialized.')


#  models
class SubmitRecord(db.Model):
    __tablename__ = 'submit_record'
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32))
    task_id = db.Column(db.Integer, index=True)
    file_name = db.Column(db.String())
    state = db.Column(db.String())
    result = db.Column(db.Text)
    error = db.Column(db.Text)


#  views
@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    # if form.validate_on_submit():
    if form.is_submitted():  # fixme
        file = form.file.data
        api = RequestApi(file)
        # api.call()
        record = SubmitRecord.query.filter_by(file_hash=api.file_hash).first()
        if record:
            flash('文件已经识别过了哦～，可以在下面的列表里找到。文件名：{}'.format(record.file_name))
        else:
            record = SubmitRecord(file_hash=api.file_hash, task_id=api.task_id, file_name=api.file_name, state='上传成功')
            db.session.add(record)
            db.session.commit()
            flash('上传成功，请稍候哦~')
    records = SubmitRecord.query.all()
    return render_template('index.html', form=form, records=records)


@app.route('/progress', methods=['POST'])
def get_progress():
    task_id = int(request.form['task_id'])
    result = RequestApi.get_progress(task_id)
    if result['err_no'] != 0 and result['err_no'] != 26605:
        print('task error: ' + result['failed'])
        return 'fail'
    else:
        status = json.loads(result['data'])
        if status['status'] == 9:
            return 'success'
    return 'in_progress'


@app.route('/result', methods=['POST'])
def get_result():
    task_id = int(request.form['task_id'])
    # result = RequestApi.get_result(task_id)
    return 'success'


if __name__ == '__main__':
    app.run()

