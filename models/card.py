from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card', cascade='all, delete')


class CardSchema(ma.Schema):
  # tell marshmallow to use UserSchema to serialize the 'user' field
  user = fields.Nested('UserSchema', exclude=['password', 'cards', 'comments'])
  # wrapped in a list because many comments
  comments = fields.List(fields.Nested('CommentSchema', exclude=['card', 'id']))
  # validation
  title = fields.String(required=True)

  class Meta:
    # add user and comments for jsonify output in marshmallow
    fields = ('id', 'title', 'description', 'status', 'user','comments')
    ordered = True