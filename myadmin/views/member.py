# 员工信息管理视图文件
from datetime import datetime

from django.core.paginator import Paginator

from django.shortcuts import render

from myadmin.models import Member


# Create your views here.

def index(request, pIndex=1):
    # 浏览信息
    umod = Member.objects
    ulist = umod.filter(status__lt=9)
    # 获取并判断搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(nickname__contains=kw)
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

    context = {'memberlist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpage': maxpages, "mywhere": mywhere}
    return render(request, 'myadmin/member/index.html', context)


def delete(request, mid=0):
    # 执行信息删除
    try:
        ob = Member.objects.get(id=mid)
        ob.status = 9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, 'myadmin/info.html', context)
