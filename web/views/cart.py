from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


# 添加购物车
def add(request, pid):
    # 从session中获取当前店铺所有菜品信息，并从中获取要放入购物车的菜品
    product = request.session['productlist'][pid]
    product['num'] = 1  # 初始化当前菜品购买量
    # 尝试从session中获取名字为cartlist的购物车信息
    cartlist = request.session.get("cartlist", {})
    if pid in cartlist:
        cartlist[pid]['num'] += product['num']
    else:
        cartlist[pid] = product
    # 将cartlist放入购物车放入到session中
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))


# 删除购物车
def delete(request, pid):
    # 尝试从session中获取名字为cartlist的购物车信息
    cartlist = request.session.get("cartlist", {})
    del cartlist[pid]
    # 将cartlist放入购物车放入到session中
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))


# 清除购物车
def clear(request):
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))


# 更改购物车
def change(request):
    # 尝试从session中获取名字为cartlist的购物车信息
    cartlist = request.session.get("cartlist", {})
    pid = request.GET.get("pid", 0)  # 菜品id
    m = int(request.GET.get('num', 1))  # 要修改的数量
    if m < 1:
        m = 1
    cartlist[pid]['num'] = m
    # 将cartlist放入购物车放入到session中
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))
