# 员工信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from myadmin.models import User


# Create your views here.

def index(request, pIndex=1):
    # 浏览信息
    umod = User.objects
    ulist = umod.filter(status__lt=9)
    # 获取并判断搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword=' + kw)
    # 执行分页
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 每页5条数据
    maxpages = page.num_pages  # 获取最大页数
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    context = {'userlist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpage': maxpages, "mywhere": mywhere}
    return render(request, 'myadmin/user/index.html', context)


def add(request):
    # 加载信息添加表单
    pass


def insert(request):
    # 执行信息添加
    pass


def delete(request, uid=0):
    # 执行信息删除
    pass


def edit(request, uid=0):
    # 编辑表单
    pass


def update(request, uid=0):
    # 执行信息编辑
    pass
