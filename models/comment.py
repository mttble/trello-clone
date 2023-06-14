from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text())
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='comments')

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id", ondelete='CASCADE'), nullable=False)
    card = db.relationship('Card', back_populates='comments')


class CommentSchema(ma.Schema):
  # tell marshmallow to use UserSchema to serialize the 'user' field
  user = fields.Nested('UserSchema', only=['name', 'email', 'is_admin'])
  card = fields.Nested('CardSchema', only=['title', 'description', 'status'])

  class Meta:
    fields = ('id', 'message', 'date_created', 'user', 'card')
    ordered = True