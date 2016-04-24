#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup


def get_formhash():
    """ Get formhash from editorForm"""
    # Set request form header info
    request_form_header = {
        'Host': 'translate.chinadaily.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://translate.chinadaily.com.cn/portal.php?mod=portalcp&ac=article',
        'Cookie': 'q8vf_2132_saltkey=KM66kb68; q8vf_2132_lastvisit=1461328499; q8vf_2132_lastact=1461368884%09api.php%09js; pgv_pvi=8652438736; y50Z_2132_sid=Y0ZqO3; y50Z_2132_saltkey=RKJKzlKC; y50Z_2132_lastvisit=1461340300; y50Z_2132_lastact=1461370676%09home.php%09editor; y50Z_2132_ulastactivity=9ed5RRxYlU46SB6r%2Fx%2BfHJ4utl3rFSX2fmP%2FpVIRaV2KdUbWtBQg; y50Z_2132_auth=0b93paD3LXW4VVHpolwb8l2VW%2Fe9y04IaPq6fBly9dVCSEFTM4vRzbLPbZijpKI2YJZXJavStNk3qChQqKrjWsJDjSZe; y50Z_2132_lastcheckfeed=1603783%7C1461343917; y50Z_2132_security_cookiereport=5669fYPwe%2FOau0wELTn%2BCGZpw7IaPYJu4gRuGyE%2B8V9CZd1QfcGc; pgv_info=ssi=s869159533; y50Z_2132_sendmail=1; y50Z_2132_checkpm=1; tjpctrl=1461372601633',
        'DNT': '1',
        'Connection': 'keep-alive'
    }

    # Get formhash from response
    response = requests.get('http://translate.chinadaily.com.cn/portal.php?mod=portalcp&ac=article',
                            headers=request_form_header)

    soup = BeautifulSoup(response.content, 'html.parser')
    formhash_tag = soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']

    return formhash


def post_article(form_hash, boundary, title, summary, content):
    """ Post article """
    # Construct request_form_header
    post_form_header = {
        'Host': 'translate.chinadaily.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://translate.chinadaily.com.cn/portal.php?mod=portalcp&ac=article',
        'Cookie': 'q8vf_2132_saltkey=KM66kb68; q8vf_2132_lastvisit=1461328499; q8vf_2132_lastact=1461368884%09api.php%09js; pgv_pvi=8652438736; y50Z_2132_sid=Y0ZqO3; y50Z_2132_saltkey=RKJKzlKC; y50Z_2132_lastvisit=1461340300; y50Z_2132_lastact=1461370676%09home.php%09editor; y50Z_2132_ulastactivity=9ed5RRxYlU46SB6r%2Fx%2BfHJ4utl3rFSX2fmP%2FpVIRaV2KdUbWtBQg; y50Z_2132_auth=0b93paD3LXW4VVHpolwb8l2VW%2Fe9y04IaPq6fBly9dVCSEFTM4vRzbLPbZijpKI2YJZXJavStNk3qChQqKrjWsJDjSZe; y50Z_2132_lastcheckfeed=1603783%7C1461343917; y50Z_2132_security_cookiereport=5669fYPwe%2FOau0wELTn%2BCGZpw7IaPYJu4gRuGyE%2B8V9CZd1QfcGc; pgv_info=ssi=s869159533; y50Z_2132_sendmail=1; y50Z_2132_checkpm=1; tjpctrl=1461372601633',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary
    }

    # Post data
    post_data = {
        'title': title,
        'summary': summary,
        'content': content,
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


def add_article(title, summary, content):
    # predefined boundary
    boundary = '---------------------------1660470091365'

    # Get form hash first
    form_hash = get_formhash()

    # post our aritlce now
    response = post_article(form_hash, boundary, title, summary, content)

    return response


if __name__ == '__main__':
    # Set boundary
    boundary = '---------------------------1660470091365'

    form_hash = get_formhash()

    response = post_article(form_hash, boundary)

    print response.status_code

    with open('/tmp/final.html', 'w') as outfile:
        outfile.write(response.content)
