# 菜品信息管理视图文件
from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from myadmin.models import Product, Shop, Category
import time,os

# Create your views here.

def index(request, pIndex=1):
    # 浏览信息
    umod = Product.objects
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
    page = Paginator(ulist,10)  # 每页10条数据
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
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name

    context = {'productlist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpage': maxpages, "mywhere": mywhere}
    return render(request, 'myadmin/product/index.html', context)


def add(request):
    # 获取当前所有店铺信息
    slist = Shop.objects.values('id', 'name')
    context = {'shoplist': slist}
    return render(request, 'myadmin/product/add.html', context)


def insert(request):
    # 执行信息添加
    try:
        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.category_id = request.POST['category_id']
        ob.price = request.POST['price']
        # 封面图片上传
        myfile = request.FILES.get('cover_pic', '')
        if not myfile:
            return HttpResponse("没有菜品封面上传文件信息")
        cover_pic = str(time.time()) + '_' + myfile.name.split('_').pop()
        destination = open('./static/uploads/product/' + cover_pic, 'wb+')
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        ob.status = 1
        ob.cover_pic = cover_pic
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, 'myadmin/info.html', context)


def delete(request, pid=0):
    # 执行信息删除
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, 'myadmin/info.html', context)


def edit(request, pid=0):
    # 编辑表单
    try:
        ob = Product.objects.get(id=pid)
        context = {'product': ob}
        # 获取当前所有店铺信息
        slist = Shop.objects.values('id', 'name')
        context['shoplist'] = slist
        return render(request, 'myadmin/product/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息"}
        return render(request, 'myadmin/info.html', context)


def update(request, pid=0):
    # 执行信息编辑
    try:
        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.category_id = request.POST['category_id']
        ob.price = request.POST['price']
        # 获取原图片
        oldpicname = request.POST['oldpicname']
        # 封面图片上传
        myfile = request.FILES.get('cover_pic', '')
        if not myfile:
            cover_pic = oldpicname
        else:
            cover_pic = str(time.time()) + '_' + myfile.name.split('_').pop()
            destination = open('./static/uploads/product/' + cover_pic, 'wb+')
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "修改成功"}
        # 判断并删除老图片
        if myfile:
            os.remove('./static/uploads/product/' + oldpicname)

    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
        if myfile:
            os.remove('./static/uploads/product/' + cover_pic)
    return render(request, 'myadmin/info.html', context)
