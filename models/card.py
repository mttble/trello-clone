from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# Validation for status field doing OneOf
VALID_STATUSES = ['To Do', 'Done', 'In Progress', 'Testing', 'Deployed']

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
  title = fields.String(required=True, validate=And(
     Length(min=3, error='Title must be at least 3 characters long'),
     Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')
     ))
  description = fields.String(load_default='')
  status = fields.String(load_default=VALID_STATUSES[0])
  # status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))

  @validates_schema()
  def validate_status(self, data, **kwargs):
     status = [x for x in VALID_STATUSES if x.upper() == data['status'].upper()]
     if len(status) == 0:
        raise ValidationError(f'Status must be one of: {VALID_STATUSES}')
     data['status'] = status[0]

  class Meta:
    # add user and comments for jsonify output in marshmallow
    fields = ('id', 'title', 'description', 'status', 'user','comments')
    ordered = True