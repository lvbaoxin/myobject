# 员工信息管理视图文件
from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from myadmin.models import Category, Shop


# Create your views here.

def index(request, pIndex=1):
    # 浏览信息
    umod = Category.objects
    ulist = umod.filter(status__lt=9)
    # 获取并判断搜索条件
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 执行分页
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 每页10条数据
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

    context = {'categorylist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpage': maxpages, "mywhere": mywhere}
    return render(request, 'myadmin/category/index.html', context)


def loadCategory(request, sid):
    clist = Category.objects.filter(status__lt=9, shop_id=sid).values("id", 'name')
    return JsonResponse({'data': list(clist)})


def add(request):
    # 获取当前所有店铺信息
    slist = Shop.objects.values('id', 'name')
    context = {'shoplist': slist}
    return render(request, 'myadmin/category/add.html', context)


def insert(request):
    # 执行信息添加
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        #  将当前员工信息的密码做MD5值
        ob.status = 1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, 'myadmin/info.html', context)


def delete(request, cid=0):
    # 执行信息删除
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, 'myadmin/info.html', context)


def edit(request, cid=0):
    # 编辑表单
    try:
        ob = Category.objects.get(id=cid)
        context = {'category': ob}
        # 获取当前所有店铺信息
        slist = Shop.objects.values('id', 'name')
        context['shoplist'] = slist
        return render(request, 'myadmin/category/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息"}
        return render(request, 'myadmin/info.html', context)


def update(request, cid=0):
    # 执行信息编辑
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改"}
    return render(request, 'myadmin/info.html', context)
