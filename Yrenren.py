import cookielib
import re
import urllib
import urllib2


class Yrenren:
    def __init__(self, email='', password=''):
        self.email = email
        self.password = password

    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        post_data = urllib.urlencode({
            'email': self.email,
            'password': self.password
        })
        req = urllib2.Request("http://www.renren.com/PLogin.do", post_data)
        res = urllib2.urlopen(req)

    def post_status(self, status):
        re_rtk = re.compile("get_check_x:'(.*?)'")
        re_request_token = re.compile("get_check:'(.*?)'")
        re_hostid = re.compile("hostid=(\d+)")

        content = urllib2.urlopen("http://www.renren.com").read()
        rtk = re_rtk.search(content).group(1)
        request_token = re_request_token.search(content).group(1)
        hostid = re_hostid.search(content).group(1)
        post_url = 'http://shell.renren.com/%s/status' % hostid

        post_data = urllib.urlencode({
            'content': status,
            'hostid': hostid,
            '_rtk': rtk,
            'requestToken': request_token,
            'channel': "renren"
        })
        req = urllib2.Request(post_url, post_data)
        res = urllib2.urlopen(req)
