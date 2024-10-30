from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    module_code = db.Column(db.String(10))
    