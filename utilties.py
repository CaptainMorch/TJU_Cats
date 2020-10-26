import logging
from copy import copy
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from django.urls import path
from django.conf import settings
from django.utils.module_loading import import_string


class ChoiceList:
    """
    用于辅助编写模型 Field 中 choices 值的类。
    最好实例化为模型类的类常量，以便日后使用。
    注意：实例被更改后，需要重新进行 migrate 操作
    """

    def __init__(self, *args, null=False):
        """
        实例化时可传入任意个位置参数，每个均可为单个选项或选项集；
        如允许 null，则可设置 null='提示语'，设置为 True 则默认为'未知'
        """
        self.choices = []
        self.null = null

        for each in args:
            if hasattr(each, "__iter__") and not isinstance(each, str):
                self.choices.extend(list(each))
            else:
                self.choices.append(each)

    def to_turples(self):
        """返回一个由 (序号: 选项) 样式元组组成的列表。用于 choices 属性"""
        turples = []
        num = 0
        for choice in self.choices:
            num += 1
            turples.append((num, choice))
        if self.null:
            turples.append((None, self.null if isinstance(self.null, str) else '未知'))
        return turples


    def get_val(self, choice):
        """传入选项返回序号值。用在需要从数据库查找值时"""
        if choice in self.choices:
            return self.choices.index(choice) + 1
        else:
            raise ValueError(f'{choice} 不是一个正确的选项。')


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


def actions_urlpatterns(*args, namespace='action'):
    """
    Helper Function, receive a bunch of Action subclasses
    and return a namespaced urlpatterns of them.
    """
    paths = []
    for action in args:
        paths.append(path(action.get_name(), action.as_view(), name=action.get_name()))
    return (paths, namespace)


def setting(option):
    """加载并返回一个设置值"""
    return getattr(settings, option.upper())
