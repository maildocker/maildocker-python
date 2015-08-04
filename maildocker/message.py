import base64
from email.utils import formatdate, parseaddr
import json
from mimetypes import guess_type


class Mail(object):

    """Maildocker Message Class"""

    to = []
    cc = []
    bcc = []
    images = []
    attachments = []
    merge_vars = {}
    mail_from = None

    def __init__(self, **opts):
        """
        Constructs Maildocker Message object.
        Args:
            to: Recipient
            cc: Copied recipient
            bcc: Blind copied recipient
            from: Sender
            subject: Email title
            template: Maildocker Template name
            text: Email text body
            html: Email html body
            reply_to: Reply address
            date: Origin date
            headers: Optional headers
            attachments: Files to attach
            images: Images to attach
        """
        self.set_from(opts.get('mail_from', ''))
        self.add_to(opts.get('to', []))
        self.add_cc(opts.get('cc', []))
        self.add_bcc(opts.get('bcc', []))
        self.add_vars(opts.get('merge_vars', {}))
        self.set_subject(opts.get('subject', ''))
        self.set_template(opts.get('template', ''))
        self.set_text(opts.get('text', ''))
        self.set_html(opts.get('html', ''))
        self.set_replyto(opts.get('reply_to', ''))
        self.add_attachment(opts.get('attachments', []))
        self.add_image(opts.get('images', []))
        self.set_headers(opts.get('headers', ''))
        self.set_date(opts.get('date', formatdate()))

    def set_from(self, mail_from):
        name, email = parseaddr(mail_from.replace(',', ''))
        self.mail_from = {'email': email}
        if name:
            self.mail_from.update({'name': name})

    def add_mail(self, field, mail, merge_vars=None):
        if isinstance(mail, str):
            name, email = parseaddr(mail.replace(',', ''))
            mail = {'email': email}
            if name:
                mail.update({'name': name})
            if merge_vars:
                mail.update({'merge_vars': merge_vars})
            field.append(mail)
        elif hasattr(mail, '__iter__'):
            for email in mail:
                self.add_mail(field, email)

    def add_to(self, to, merge_vars=None):
        self.add_mail(self.to, to, merge_vars)

    def add_cc(self, cc, merge_vars=None):
        self.add_mail(self.cc, cc, merge_vars)

    def add_bcc(self, bcc, merge_vars=None):
        self.add_mail(self.bcc, bcc, merge_vars)

    def add_vars(self, merge_vars):
        self.merge_vars.update(merge_vars)

    def set_subject(self, subject):
        self.subject = subject

    def set_template(self, template):
        self.template = template

    def set_text(self, text):
        self.text = text

    def set_html(self, html):
        self.html = html

    def set_replyto(self, replyto):
        self.reply_to = replyto

    def set_date(self, date):
        self.date = date

    def set_headers(self, headers):
        if isinstance(headers, str):
            self.headers = headers
        else:
            self.headers = json.dumps(headers)

    def add_file(self, field, _file):
        if isinstance(_file, dict):
            field.append(_file)
        else:
            if isinstance(_file, str):
                _file = open(_file, 'rb')
            field.append({
                'name': _file.name,
                'type': guess_type(_file.name)[0],
                'content': base64.b64encode(_file.read())
            })

    def add_attachment(self, attachment):
        if not isinstance(attachment, list):
            attachment = [attachment]
        for _file in attachment:
            self.add_file(self.attachments, _file)

    def add_image(self, image):
        if not isinstance(image, list):
            image = [image]
        for _file in image:
            self.add_file(self.images, _file)
