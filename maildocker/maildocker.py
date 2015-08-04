import base64
import json
from socket import timeout
import urllib2

from version import __version__


class MaildockerClient(object):

    """Maildocker API Class"""

    def __init__(self, api_key, api_secret, **opts):
        """
        Construct Maildocker API object.
        Args:
            api_key: Maildocker Docklet api_key
            api_secret: Maildocker Docklet api_secret
        """

        self.api_key = api_key
        self.api_secret = api_secret

        self.host = opts.get('host', 'https://ecentry.io')
        self.port = str(opts.get('port', '443'))
        self.endpoint = opts.get(
            'endpoint', '/api/maildocker/' + __version__ + '/mail/'
        )
        self.mail_url = self.host + ':' + self.port + self.endpoint
        self._raise_errors = opts.get('raise_errors', False)
        self.proxies = opts.get('proxies', None)

    def _build_body(self, message):
        values = {
            'to': message.to,
            'cc': message.cc,
            'bcc': message.bcc,
            'merge_vars': message.merge_vars,
            'from': message.mail_from,
            'subject': message.subject,
            'template': message.template,
            'text': message.text,
            'html': message.html,
            'reply_to': message.reply_to,
            'headers': message.headers,
            'date': message.date,
            'attachments': message.attachments,
            'images': message.images
        }

        for k in list(values.keys()):
            if not values[k]:
                del values[k]
        return values

    def _make_request(self, message):
        if self.proxies:
            proxy_support = urllib2.ProxyHandler(self.proxies)
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        data = json.dumps(self._build_body(message))
        req = urllib2.Request(self.mail_url, data)
        req.add_header('Content-Type', 'application/json')

        base64string = base64.encodestring(
            self.api_key + ':' + self.api_secret
        ).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)

        response = urllib2.urlopen(req, timeout=10)
        body = response.read()
        return response.getcode(), json.loads(body)

    def send(self, message):
        try:
            return self._make_request(message)
        except urllib2.HTTPError as e:
            return e.code, e.read()
        except timeout as e:
            return 408, e
