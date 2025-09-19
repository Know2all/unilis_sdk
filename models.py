from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    invoice_id = db.Column(db.Integer,nullable=False)
    callback_url = db.Column(db.String(500),nullable=False)

    def to_dict(self):
        return {"id":self.id,"invoice_id":self.invoice_id,"callback_url":self.callback_url}
