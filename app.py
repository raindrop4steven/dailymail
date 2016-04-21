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
    body = soup.find(itemprop="articleBody")
    body_soup = BeautifulSoup(str(body), 'html.parser')

    extracted_body = body_soup.find_all(need_extract)

    return title, str(extracted_body)


def need_extract(tag):
    """ Check if tag needed.
    1. <div class=moduleFull>
    2. <div class=moduleFull mol-video
    3. <div class=mol-page-break
    4. <div class=art-ins mol-factbox news
    5. <div>: facebook news, don't know why no class
    """

    result = True
    # filter rules to rule out these elements
    rules = ['moduleFull',
             'vjs-video-container',
             'mol-page-break',
             'art-ins']

    if tag.name == 'div':
        if tag.has_attr('class') and tag['class'][0] in rules:
            result = False
        elif not tag.has_attr('class'):
            result = False

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
