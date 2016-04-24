#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import requests
from bs4 import BeautifulSoup


def get_formhash():
    """ Get formhash from editorForm"""

    # Get common headers first
    request_form_header = get_common_header()

    # Add special header for GET
    request_form_header['DNT'] = '1'

    # Get formhash from response
    response = requests.get('http://translate.chinadaily.com.cn/portal.php?mod=portalcp&ac=article',
                            headers=request_form_header)

    soup = BeautifulSoup(response.content, 'html.parser')
    formhash_tag = soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']

    return formhash


def post_article(form_hash, boundary, fromurl, title, summary, content):
    """ Post article """
    # Construct request_form_header
    post_form_header = get_common_header()
    post_form_header['Content-Type'] = ('multipart/form-data; boundary=%s' % boundary)

    # Post data
    post_data = {
        'title': title,
        'summary': summary,
        'content': content,
        'fromurl': fromurl,
        'catid': '7',
        'attach_ids': '0',
        'articlesubmit': 'true',
        'formhash': str(form_hash)
    }

    coded_params = encode_multipart(post_data, boundary)

    # Post article now
    response = requests.post('http://translate.chinadaily.com.cn/portal.php?mod=portalcp&ac=article',
                             headers=post_form_header, data=coded_params)

    return response


def encode_multipart(params_dict, boundary):
    """ Encode a multipart/form-data body with given boundary"""
    data = []

    for k, v in params_dict.items():
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
        data.append(v if isinstance(v, str) else v.decode('utf-8'))

    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data)


def add_article(fromurl, title, summary, content):
    # predefined boundary
    boundary = '---------------------------1660470091365'

    # Get form hash first
    form_hash = get_formhash()

    # post our aritlce now
    response = post_article(form_hash, boundary, fromurl, title, summary, content)

    return response


def get_common_header():
    """ Get common header from config.ini """
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    headers = cf.items('headers')

    return dict(headers)

if __name__ == '__main__':
    # Set boundary
    boundary = '---------------------------1660470091365'

    form_hash = get_formhash()

    response = post_article(form_hash, boundary)

    print response.status_code

    with open('/tmp/final.html', 'w') as outfile:
        outfile.write(response.content)
