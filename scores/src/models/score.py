from marshmallow import  Schema, fields
from sqlalchemy import Column, Float
from .model import Model, Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Score(Model, Base):
  __tablename__ = 'scores'

  offerId = Column(UUID(as_uuid=True), default=uuid.uuid4)
  utility = Column(Float)

  def __init__(self, offerId, utility):
    Model.__init__(self)
    self.offerId = offerId
    self.utility = utility

class ScoreSchema(Schema):
  id = fields.UUID()
  createdAt = fields.DateTime()
  offerId = fields.UUID()
  utility = fields.Float()