#!/usr/bin/env python
# encoding: utf-8

from DSql import DSql

if __name__ == '__main__':
    sql_handler = DSql()

    # insert new article
    sql_handler.insert_article(link='this/is/a/test/link/with/random/length/')

    # duplicate insert
    sql_handler.insert_article(link='this/is/a/test/link/with/random/length/')

    # very long insert
    long_link = 'http://www.dailymail.co.uk/news/article-3517608/I-dropped-knees-started-giving-chest-compressions-spit-water-thought-going-wake-Nick-Gordon-breaks-silence-Bobbi-Kristina-s-tragic-drowning-reveals-PREGNANT-twice.html'
    sql_handler.insert_article(link=long_link)

    # null link insert
    null_link = None
    sql_handler.insert_article(link=null_link)

    # emtpy link insert
    empty_link = ''
    sql_handler.insert_article(link=empty_link)

    # query article
    result1 = sql_handler.query_article(link='this/is/a/test/link/with/random/length/')
    result2 = sql_handler.query_article(link='this/is/a/test/link/with/random/length/2/')
    result3 = sql_handler.query_article(link=long_link)

    print result1
    print result2
    print result3
