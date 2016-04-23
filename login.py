#!/usr/bin/env python
# encoding: utf-8

import requests
import ConfigParser
import pprint


def create_session():
    # Open config.ini
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')

    # Get cookies items
    cookies_item = cf.items('cookies')
    cookies = dict(cookies_item)

    pprint.pprint(cookies)

    # Sessions
    # session = requests.session()

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

    return response

if __name__ == '__main__':
    response = create_session()

    with open('/tmp/out.html', 'w') as outfile:
        outfile.write(response.content)
