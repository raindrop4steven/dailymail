#!/usr/bin/env python
# encoding: utf-8

import os
import datetime
import urllib
from bs4 import BeautifulSoup


def get_content_from_url(url):
    """ Get content from specified url"""
    response = None
    if url is not None:
        response = urllib.urlopen(url)

    return response


def get_article_list(html_doc):
    """ Get article list from index.html"""
    DOMAIN_NAME = 'http://www.dailymail.co.uk'

    urls = []

    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.select('.linkro-darkred > a')

    for url in links:
        if url.has_attr('href'):
            href = DOMAIN_NAME + url['href']
            urls.append(href)

    return urls


def get_title_and_content(html_doc):
    """ Get article title and body """
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Get title first
    title = soup.find(id='js-article-text').find('h1').string

    # Clean article body first, remove videos, share links etc.
    body = soup.find(itemprop="articleBody").encode('ascii')

    body_soup = BeautifulSoup(body, 'html.parser')

    extracted_body = body_soup.find_all(cut_rules)

    return title, ''.join(x.encode('ascii') for x in extracted_body)


def cut_rules(tag):
    """ Get needed tag
    1. <p>
    2. <div class=artSplitter>
    """
    result = False

    rules = ['mol-img']

    if tag.name == 'p' or tag.name == 'div' and tag.has_attr('class') and tag['class'][0] in rules:
        result = True

    return result


if __name__ == '__main__':

    # set download folder
    ROOT_FOLDER = '/home/steven/dailymail'
    ARTICLE_FOLDER = os.path.join(ROOT_FOLDER, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    if not os.path.exists(ROOT_FOLDER):
        os.mkdir(ROOT_FOLDER)

    if not os.path.exists(ARTICLE_FOLDER):
        os.mkdir(ARTICLE_FOLDER)

    # Index url contains our article links
    index_url = 'http://www.dailymail.co.uk/ushome/index.html'
    response = get_content_from_url(index_url).read()

    # Get article links
    links = get_article_list(response)

    # Iterate links
    for idx, url in enumerate(links):
        # filename
        fname = os.path.join(ARTICLE_FOLDER, str(idx))

        # Get response and parse
        response = get_content_from_url(url).read()
        try:
            title, content = get_title_and_content(response)

            with open(fname, 'w') as file:
                file.write('<h1>{0}</h1>\n{1}'.format(title, content))
                print ('Success : {0}'.format(idx))

        except Exception as e:
            print ('Error : {0}'.format(idx))
