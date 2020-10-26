import logging
from copy import copy
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from django.conf import settings
from django.utils.module_loading import import_string


class ServerChanHandler(logging.Handler):
    """logging handler，将错误日志通过方糖推送到微信"""

    def __init__(self, sckey=None, reporter_class=None):
        super().__init__()
        self.sckey = sckey or settings.SERVER_CHAN_SCKEY
        self.reporter_class = import_string(reporter_class or settings.DEFAULT_EXCEPTION_REPORTER)

    def emit(self, record):
        """发送日志"""

        #
        # COPY from django.utils.log.AdminEmailHandler:
        #

        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = self.reporter_class(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (self.format(no_exc_record), reporter.get_traceback_text())

        # 
        # COPY END
        #

        data = {'text': '来来来修 bug 了', 'desp': message}
        request = Request(
            url=f'https://sc.ftqq.com/{self.sckey}.send',
            data=urlencode(data).encode(),
            method='POST'
            )
        urlopen(request)
        
    def format_subject(self, subject):
        """
        Escape CR and LF characters.

        COPIED FROM django.log.utils.log.AdminEmailHandler
        """
        return subject.replace('\n', '\\n').replace('\r', '\\r')