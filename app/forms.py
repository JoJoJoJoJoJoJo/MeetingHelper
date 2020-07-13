from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class UploadSet:

    def __init__(self, extensions):
        self.extensions = extensions or []

    def file_allowed(self, file, filename):
       return bool(file and filename)

    def __getitem__(self, item):
        return self.extensions[item]

    def __iter__(self):
        return self.extensions.__iter__()


class FileForm(FlaskForm):
    file = FileField('录音文件', validators=[DataRequired(), FileAllowed(UploadSet(['wav', 'flac', 'opus', 'm4a', 'mp3']), '文件格式不对哦～')])
    submit = SubmitField('提交')
