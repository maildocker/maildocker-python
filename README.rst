Maildocker-Python
=================

This library allows you to quickly and easily send emails through
Maildocker using Python.

Example
-------

.. code:: python

    import maildocker

    md = maildocker.MaildockerClient(
        api_key='0cc175b9c0f1b6a831c',
        api_secret='92eb5ffee6ae2fec3ad'
    )

    message = maildocker.Mail(
        mail_from='Maildocker <maildocker@ecentry.io>',
        to='John Snow <john.snow@thrones.com>',
        subject='maildocker-python-library',
        text='**{{system}}** ({{url}})',
        merge_vars={'system': 'Maildocker', 'url': 'http://maildocker.io'},
        attachments=[
            {'name': 'plaintext.txt', 'type': 'text/plain', 'content': 'dHN0'},
            'spreadsheet.xls'
        ]
    )

    http_status, response = md.send(message)

    # OR

    message = maildocker.Mail()

    message.set_from('Maildocker <maildocker@ecentry.io>')
    message.add_to('John Snow <john.snow@thrones.com>')
    message.set_subject('maildocker-python-library')
    message.set_text('**{{system}}** ({{url}})')
    message.add_vars({'system': 'Maildocker', 'url': 'http://maildocker.io'})
    message.add_attachment([
        {'name': 'plaintext.txt', 'type': 'text/plain', 'content': 'dHN0'},
        'spreadsheet.xls'
    ])

    http_status, response = md.send(message)
