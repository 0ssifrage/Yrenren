import cookielib
import json
import re
import urllib
import urllib2


class Yrenren:
    def __init__(self, email='', password=''):
        self.email = email
        self.password = password
        self.re_rtk = re.compile("get_check_x:'(.*?)'")
        self.re_request_token = re.compile("get_check:'(.*?)'")
        self.re_hostid = re.compile("hostid=(\d+)")
        self.fetched = False

    def fetch_data(self):
        if self.fetched:
            return
        content = urllib2.urlopen("http://www.renren.com").read()
        self.rtk = self.re_rtk.search(content).group(1)
        self.request_token = self.re_request_token.search(content).group(1)
        self.hostid = self.re_hostid.search(content).group(1)
        self.fetched = True

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
        self.fetch_data()

        post_url = 'http://shell.renren.com/%s/status' % self.hostid
        post_data = urllib.urlencode({
            'content': status.encode('utf-8'),
            'hostid': self.hostid,
            '_rtk': self.rtk,
            'requestToken': self.request_token,
            'channel': "renren"
        })
        req = urllib2.Request(post_url, post_data)
        res = urllib2.urlopen(req).read()
        res = json.loads(res)
        status_id = int(float(res["updateStatusId"]))
        return status_id

    def reply_status(self, entry_id, entry_owner_id, reply_content):
        self.fetch_data()

        post_url = 'http://comment.renren.com/comment/xoa2/create'
        post_data = urllib.urlencode({
            'content': reply_content.encode('utf-8'),
            'type': 'status',
            'entryId': entry_id,
            'entryOwnerId': entry_owner_id,
            'requestToken': self.request_token,
            '_rtk': self.rtk,
        })
        req = urllib2.Request(post_url, post_data)
        res = urllib2.urlopen(req)
