from django import forms
from .models import Comment

# 创建评论表单
class CommentForm(forms.ModelForm):
    # 指定表单相关信息
    class Meta:
        # 指定表单对应的数据模型是Comment类
        model = Comment
        # 指定表单需要显示的数据（数据来自Comment数据模型类）
        fields = ['name', 'email', 'url', 'text']
