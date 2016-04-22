#!/usr/bin/env python
# encoding: utf-8

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
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.select('.linkro-darkred > a')

    return links


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

    # Index url contains our article links
    # url = 'http://www.dailymail.co.uk/ushome/index.html'
    # response = get_content_from_url(url)
    # content = response.read()

    # Get article links
    # links = get_article_list(content)

    # Content url
    content_url = 'http://www.dailymail.co.uk/news/article-3550828/He-walks-like-George-William-Harry-poke-fun-clip-father-toddler-Royals-gather-watch-never-seen-home-videos-Queen-90th-birthday-special.html'

    response = get_content_from_url(content_url).read()

    title, content = get_title_and_content(response)

    with open('/tmp/out.html', 'w') as file:
        file.write('{0}\n{1}'.format(title, content))
