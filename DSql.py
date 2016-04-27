#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql import Article, Base


class DSql(object):
    """ DSql handles all the sql operations. """
    def __init__(self):
        self.engine = create_engine('sqlite:///dailymail.db')
        # Create all
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def insert_article(self, link):
        """ Add new link """
        # Check link nullable, actually it should not happend
        if link is not None and len(link) > 0:
            # Check if link already exists
            article = self.session.query(Article).filter(Article.link == link).first()

            # Don't do any error, since its not important here
            if article is None:
                article = Article(link=link)
                self.session.add(article)
                self.session.commit()

    def query_article(self, link):
        """ Query a link """
        article = self.session.query(Article).filter(Article.link == link).first()

        return article is None
