# 菜品信息管理视图文件
from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from myadmin.models import Product, Shop, Category, Orders ,Member
import time, os


# Create your views here.

def index(request, pIndex=1):
    # 浏览信息
    umod = Orders.objects
    ulist = umod.filter(status__lt=9)
    # 获取并判断搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取并判断类别搜索条件
    cid = request.GET.get('category_id', None)
    if cid:
        ulist = ulist.filter(category_id=cid)
        mywhere.append('category_id_=' + cid)
    # 执行分页
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 每页10条数据
    maxpages = page.num_pages  # 获取最大页数
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
        member = Member.objects.only('mobile').get(id=vo.shop_id)
        vo.membername = member.mobile

    context = {'productlist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpage': maxpages, "mywhere": mywhere}
    return render(request, 'myadmin/order/index.html', context)
