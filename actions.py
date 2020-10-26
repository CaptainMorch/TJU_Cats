from datetime import date

from django.views.generic import View
from django.urls import reverse_lazy
from django.forms import Form
from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from django.shortcuts import get_object_or_404


class ActionMixin:
    """提供对实例进行'操作'的方法"""
    model = None
    success_url = None

    @classmethod
    def has_action(cls, obj):
        """接受一个 model 实例，返回该实例是否可用于此操作的 bool"""
        if not isinstance(obj, cls.model):
            raise TypeError(f'{str(obj)} 不是 {str(cls)} 的实例')
        return True

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def validate(self):
        """验证操作及表单, 返回包含 bool 和 信息str 的元组"""
        if not self.has_action(self.object):
            return (False, '')
        else:
            form = self.get_form_class(self.object)(self.request.POST)
            if form.is_valid():
                self.post_data = form.cleaned_data
                return (True, '')
            else:
                return (False, form.errors.as_json())

    def act(self):
        """对该实例进行操作"""
        return None
        
    def get_success_url(self):
        """操作成功后的跳转链接"""
        return self.success_url or self.object.get_absolute_url()


class Action(ActionMixin, View):
    """
    代表对某实例进行的特定操作的 View
    只接受 POST 方法
    """
    http_method_names = ['post']

    model_namespace = ''
    action_namespace = ''
    name = ''
    show_name = ''
    icon_url = ''
    promote_message = ''

    @classonlymethod
    def as_view(self,**initkwargs):
        """禁止在 as_view 方法中隐式地定义子类"""
        if initkwargs:
            raise ValueError("You can't pass arguments to  the as_view method of\
                an Action class like a normal view. This is because an Action\
                will be rendered before it's as_view method is called, so you\
                must explicitly subclass it instead of doing this.")
        else:
            return super().as_view()

    def post(self, request, *args, **kwargs):
        """主功能入口"""
        self.object = self.get_object()

        success, message = self.validate()
        json_data = {'success': success}
        if success:
            self.act()
            json_data['redirect_to'] = self.get_success_url()
        else:
            json_data['message'] = message
        return JsonResponse(json_data)

    @classmethod
    def get_name(cls):
        return cls.name or cls.__name__.lower()

    @classmethod
    def get_promote_message(cls, obj):
        """返回执行操作的确认信息"""
        if cls.promote_message:
            return cls.promote_message.format(obj=obj, cls=cls)
        else:
            raise NotImplementedError('未重写 get_promote_message 方法或设置 promote_message')

    @classmethod
    def get_icon_url(cls):
        return cls.icon_url or f'{cls.model.__name__.lower()}/action-{cls.get_name()}.svg'

    @classmethod
    def get_form_class(cls, obj):
        """获取 Form 类"""
        return Form

    @classmethod
    def get_form(cls, obj):
        """返回一个 form 对象"""
        return cls.get_form_class(obj)()

    @classmethod
    def get_reverse_url(cls, obj):
        """返回该操作的 url"""
        model_nsp = cls.model_namespace or cls.model.__name__.lower()
        action_nsp = cls.action_namespace or 'action'
        return reverse_lazy(
            f'{model_nsp}:{action_nsp}:{cls.get_name()}',
            kwargs={'pk': obj.pk},
            )

    @classmethod
    def render_components(cls, obj):
        """返回带有渲染好的 name, icon_url, massage, form, post_to 键的字典"""
        return {
            'name': cls.show_name,
            'icon_url': cls.get_icon_url(),
            'message': cls.get_promote_message(obj),
            'form': cls.get_form(obj),
            'post_to': cls.get_reverse_url(obj),
        }


class SetFixedAction(Action):
    """将 field 值设置为固定值 value 的操作"""
    field = ''
    value = None
    choice = ''
    promote_message = '确定将{obj.name}的{field.verbose_name}设置为“{value}”吗？'

    @classmethod
    def get_promote_message(cls, obj):
        return cls.promote_message.format(
            obj=obj, 
            value=cls.choice or cls.value,
            field=cls.model._meta.get_field(cls.field)
            )

    @classmethod
    def has_action(cls, obj):
        super().has_action(obj)
        return not (getattr(obj, cls.field) == cls.get_value())

    @classmethod
    def get_value(cls):
        """获取需要写入的真实值"""
        if cls.value:
            return cls.value
        elif cls.choice:
            choices = getattr(cls.model, f'{cls.field}_choices'.upper())
            return choices.get_val(cls.choice)
        else:
            return NotImplementedError(f'You must set "value" or "choice"\
                or override "get_value" method of {cls.__class__.__name__}')

    def act(self):
        setattr(self.object, self.field, self.get_value())
        self.object.save()