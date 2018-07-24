import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

from comments.forms import CommentForm

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.

# 首页信息页面类视图函数
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 实现分页功能，每页展示5篇文章
    paginate_by = 5

    # 在类视图中，需要传递的模板变量字典是通过 get_context_data 获得的，
    # 所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
    def get_context_data(self, **kwargs):
        # 获取父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中，已经有了paginator,page_obj,is_paginated这三个模板变量了，直接获取就可以
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用pagination_data方法获取分页导航所需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # pagination_data返回的也是一个字典，将返回的信息更新到context中
        context.update(pagination_data)

        # 返回更新后的context,以便ListView使用context中的模板变量去渲染模板
        return context

    # 定义分页数据函数
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则返回空字典
            return {}

        # 设置当前页面的左边和右边连续的页码号，初始值为空
        left = []
        right = []
        # 标示第1页页码后面和最后一页页码前面是否需要显示为省略号
        left_has_more = False
        right_has_more = False
        # 标示是否需要显示第1页和最后一页的页码号，默认为False
        first = False
        last = False
        # 获取用户请求的当前页码
        page_number = page.number
        # 获取总页码
        total_pages = paginator.num_pages
        # 获取整个分页页码的列表
        page_range = paginator.page_range

        if page_number ==1:
            # 如果用户获取的当前页码是第一页面，则把右边的连续页码获取为显示两页，左边不变，依然为空
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                # 如果当前页码右边连续显示的页码列表内的最右边的页码比总页码减1还要小，说明右边到最后页码的中间还有页码，就要用省略号来显示
                # 可以通过right_has_more来控制
                right_has_more = True

            if right[-1] < total_pages:
                # 如果当前页码右边连续显示的页码列表内的最右边的页码比总页码小，则说明右侧连续页码里不包含最后一页，则需要显示最后一页的页码
                # 可以通过last来控制
                last = True

        elif page_number == total_pages:
            # 如果用户获取的当前页面是最后一页，那么当前页面的右侧连续页面为空，左边设置显示连续两页
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                # 如果当前页面左边连续显示的页面列表的第一个页码比2大，则说明从第一页到左侧显示的页面之间还有页面，需要显示省略号
                # 可以通过left_has_more来控制
                left_has_more =True

            if left[0] > 1:
                # 如果如果当前页面左边连续显示的页面列表的第一个页码比1大，说明最左侧的页码不是第一页，需要显示第一页的页码
                # 可以通过first来控制
                first = True
        else:
            # 如果用户请求的当前页面既不是第一页，也不是最后一页,则设置当前页面的左边和右边显示的连续页码为2个页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否显示最后一页和最后一页前面的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否显示第一页和第一页后面的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        # 生成分页信息模板变量字典
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        # 返回分页信息
        return data

# 文章详情页面函数
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 浏览详情页，调用函数，使文章阅读量加1
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     return render(request, 'blog/detail.html', context={
#         'post': post,
#         'form': form,
#         'comment_list': comment_list,
#     })
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 重写get方法是为了在获取文章详情的时候，阅读量+1
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response

    # 重写get_object方法是为了获取文章内容并进行markdown格式渲染
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])

        # 文章内容的标题被设置了锚点，
        # 点击目录中的某个标题，页面就会跳到该文章内容中标题所在的位置，
        # 这时候浏览器的 URL 显示的值可能不太美观，比如像下面的样子：
        # http://127.0.0.1:8000/post/8/#_3
        # Markdown 在设置锚点时利用的是标题的值，
        # 由于通常我们的标题都是中文，Markdown 没法处理，
        # 所以它就忽略的标题的值，而是简单地在后面加了个 _1 这样的锚点值。
        # 为了解决这一个问题，我们需要修改一下传给 extentions 的参数，其具体做法如下：

        TocExtension(slugify=slugify)

        # extensions 中的 toc 拓展不再是字符串 markdown.extensions.toc ，而是 TocExtension 的实例。
        # TocExtension 在实例化时其 slugify 参数可以接受一个函数作为参数，这个函数将被用于处理标题的锚点值。
        # Markdown 内置的处理方法不能处理中文标题，所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文。
        # 这时候标题的锚点 URL 变得好看多了:
        # http://127.0.0.1:8000/post/8/#在文中插入目录

        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    # 重写get_context_data方法是为了将评论表单、文章下面的评论列表等信息传递给模板
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


# 归档分类信息列表显示类视图函数
# def archives(request, year, month):
#
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request, 'blog/index.html',
#                   context={
#                       'post_list': post_list,
#                   })

class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))

#  分类信息列表显示类视图函数
class CategoryView(IndexView):
# def category(request, pk):
    # cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate)
    # return render(request, 'blog/index.html',
    #               context={
    #                   'post_list': post_list,
    #               })

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# 标签信息列表显示类视图函数
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

# 作者下面的文章展示类视图函数
class UserView(IndexView):
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super(UserView, self).get_queryset().filter(author=user)