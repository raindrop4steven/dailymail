#!/usr/bin/env python
# encoding: utf-8

import os
import operator
import datetime
import urllib
import ConfigParser
from bs4 import BeautifulSoup

from login import add_article


def get_content_from_url(url):
    """ Get content from specified url"""
    response = None
    if url is not None:
        response = urllib.urlopen(url)

    return response


def get_article_scores(html_doc):
    """ Get article links with scores """
    DOMAIN_NAME = 'http://www.dailymail.co.uk'
    link_dict = {}
    blacklist = get_black_list()

    soup = BeautifulSoup(html_doc, 'html.parser')

    # Get share count first
    shares = soup.select('.gr3ox > a > .linktext > .bold')

    for share in shares:
        # Get share count first
        str_share = share.string
        if str_share == '' or str_share is None:
            value = 0
        elif str_share.endswith('k'):
            value = int(float(share.text[:-1]) * 1000)
        else:
            value = int(share.text)

        # Get related link
        try:
            link = share.find_parent("div", class_="article-icon-links-container").find_previous_sibling('h2').contents[1]['href']

            # Check link validation and black list
            if link is not None and len(link) > 0:
                if not any(x in link for x in blacklist):
                    link = DOMAIN_NAME + link.strip()
                    link_dict[link] = value

        except Exception:
            pass

    # Sort our links by share number
    order_links = sorted(link_dict.items(), key=operator.itemgetter(1), reverse=True)

    return order_links


def get_title_and_content(html_doc):
    """ Get article title and body """
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Get title first
    title = soup.find(id='js-article-text').find('h1').string.strip().encode('utf-8')

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

    p_rules = ['mol-para-with-font',
               'imageCaption']

    div_rules = ['mol-img']

    if tag.name == 'p' and tag.has_attr('class') and tag['class'][0] in p_rules:
        result = True
    elif tag.name == 'div' and tag.has_attr('class') and tag['class'][0] in div_rules:
        result = True

    return result


def get_black_list():
    """ Get black list"""
    blacklist = []
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')

    # Get Debug and index url and limits
    black = cf.get('config', 'Blacklist')

    if black is not None and len(black) != 0:
        blacklist = black.split(';')

    return blacklist


if __name__ == '__main__':

    # Load config first
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')

    # Get Debug and index url and limits
    debug = cf.get('config', 'Debug')
    index_url = cf.get('config', 'Url')
    limits = cf.get('config', 'Limits')

    if debug == '1':
        # set download folder
        FOLDER_NAME = 'dailymail'
        ROOT_FOLDER = os.path.join(os.path.expanduser('~'), FOLDER_NAME)
        ARTICLE_FOLDER = os.path.join(ROOT_FOLDER, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

        if not os.path.exists(ROOT_FOLDER):
            os.mkdir(ROOT_FOLDER)

        if not os.path.exists(ARTICLE_FOLDER):
            os.mkdir(ARTICLE_FOLDER)

    # Index url contains our article links
    response = get_content_from_url(index_url).read()

    # Get article ordered links
    order_links = get_article_scores(response)

    links_count = len(order_links)

    try:
        limit_count = min(int(limits), links_count)
    except ValueError as e:
        print('[Error]: Limits field in config.ini, use total links count %d instead', links_count)
        limit_count = links_count

    print('[Total]: %d links' % links_count)
    print('[Goal]: %d links' % limit_count)

    success = 0
    failure = 0

    # Iterate links
    for idx, link in enumerate(order_links):
        # filename
        if debug == '1':
            fname = os.path.join(ARTICLE_FOLDER, str(idx) + '.html')
            debugname = os.path.join(ARTICLE_FOLDER, str(idx) + '-debug.html')

        # End to scraw if success is equal to limits
        if success >= limit_count:
            break

        # Get response and parse
        url = link[0]
        response = get_content_from_url(url).read()

        try:
            title, content = get_title_and_content(response)

            fromurl = url.encode('utf-8')

            # Post article
            post_response = add_article(fromurl=fromurl, title=title, summary=title, content=content)

            post_soup = BeautifulSoup(post_response.content, 'html.parser')
            alert_right = post_soup.select('.alert_right')

            if alert_right is not None:
                success += 1
                print ('[Success]: {0}'.format(idx))
            else:
                failure += 1
                print ('[Failure]: {0}'.format(idx))

            # Debug result file
            if debug == '1':
                with open(debugname, 'w') as outfile:
                    outfile.write(post_response.content)

        except Exception as e:
            print ('[Error]: {0}\n{1}'.format(url, e))

    print('[Finish]: Posted %d articles, failure %d' % (success, failure))
