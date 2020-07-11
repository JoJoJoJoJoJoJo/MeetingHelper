from . import db


#  models
class SubmitRecord(db.Model):
    __tablename__ = 'submit_record'
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32))
    task_id = db.Column(db.String, index=True)
    file_name = db.Column(db.String())
    state = db.Column(db.String())
    result = db.Column(db.Text)
    error_no = db.Column(db.Integer)
    error = db.Column(db.Text)

