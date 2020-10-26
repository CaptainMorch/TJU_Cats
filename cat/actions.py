from datetime import date

from django.forms import CharField, DateField
from .models import Entry, Cat
from actions import SetFixedAction, Action


class AddEntryMixin:
    """为 Action 类添加自动记录 Entry 的功能"""
    use_today = False
    key = ''

    def get_entry_dict(self):
        """获取新建 Entry 对象的 mapping 参数"""
        entry_date = date.today() if self.use_today else self.post_data['entry_date']
        return {
            'key': self.key or self.show_name,
            'cat': self.object, 
            'description': self.post_data['entry_description'],
            'user': self.request.user,
            'date': entry_date,
            }

    def act(self):
        super().act()
        entry_dict = self.get_entry_dict()
        Entry.objects.create(**entry_dict)

    @classmethod
    def get_form_class(cls, obj):
        klass = super().get_form_class(obj)
        class Form(klass):
            entry_description = CharField(label='备注', required=False)
            if not cls.use_today:
                entry_date = DateField(label='日期', initial=date.today())
        return Form

class CatMixin:
    """针对猫猫的操作"""
    model = Cat

    @classmethod
    def has_action(cls, obj):
        """离世的猫猫不可再进行操作"""
        has = super().has_action(obj)
        return has and (obj.get_status_display()!='离世')

class CatAction(AddEntryMixin, CatMixin, Action):
    """针对猫猫的常规操作"""

class SetCatFixedAction(AddEntryMixin, CatMixin, SetFixedAction):
    """设定猫猫某个状态值的操作"""


class Neuter(SetCatFixedAction):
    show_name = '绝育'
    field = 'neutered'
    value = True

class Adapt(SetCatFixedAction):
    show_name = '领养'
    field = 'status'
    choice = '已领养'

class PassAway(SetCatFixedAction):
    show_name = '离世'
    field = 'status'
    choice = '离世'

class Lost(SetCatFixedAction):
    show_name = '失踪'
    field = 'status'
    choice = '失踪'

class Home(SetCatFixedAction):
    show_name = '归家'
    field = 'status'
    choice = '在校流浪'

    @classmethod
    def has_action(cls, obj):
        has = super().has_action(obj)
        return has and (obj.get_status_display() in ['失踪', '住院'])

class Hospitalize(SetCatFixedAction):
    show_name = '住院'
    field = 'status'
    choice = '住院'

class Update(CatAction):
    show_name = '更新状态'
    use_today = True
    promote_message = '确定{obj.name}当前的状态正确无误吗？</br>将设置其状态的“上次更新时间”为现在'


enabled_actions = [Update, Neuter, Adapt, Home, Hospitalize, Lost, PassAway]