from django.urls import path

from .logging import ServerChanHandler

__all__ = ['ServerChanHandler', 'ChoiceList', 'actions_urlpatterns']


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


def actions_urlpatterns(*args, namespace='action'):
    """
    Helper Function, receive a bunch of Action subclasses
    and return a namespaced urlpatterns of them.
    """
    paths = []
    for action in args:
        paths.append(path(action.get_name(), action.as_view(), name=action.get_name()))
    return (paths, namespace)