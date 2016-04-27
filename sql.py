#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    link = Column(Text(), nullable=False)


# Create an engine that stores data in the local directory's
# dailymail.db file
# engine = create_engine('sqlite:///dailymail.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL
# Base.metadata.create_all(engine)
