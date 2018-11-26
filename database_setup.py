import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Shortener(Base):
    __tablename__ = 'shortener'

    short_link = Column(
        String(20),
        primary_key = True 
    )
    long_link = Column(
        String(100),
        nullable = False
    )
    
    # @property
    # def serialize(self):
    #     # returns object data in easily serialisable format
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'course': self.course,
    #         'description': self.description,
    #         'price': self.price,
    #     }
    

###################end#of#file###################

engine = create_engine('sqlite:///shortener.db')
Base.metadata.create_all(engine)
