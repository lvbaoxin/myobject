from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import Member, Shop


# 首页
def index(request):
    # 获取当前店铺信息
    shopinfo = request.session.get("shopinfo", None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))
    return render(request, 'mobile/index.html')


# 注册会员/登录表单
def register(request):
    return render(request, 'mobile/register.html')


# 执行注册会员/登录表单
def doRegister(request):
    """执行注册/登录"""
    # 验证短信码
    verifycode = "1234"  # request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info': '验证码错误！'}
        return render(request, "mobile/register.html", context)

    try:
        # 根据手机号码获取当前会员信息
        member = Member.objects.get(mobile=request.POST['mobile'])
    except Exception as err:
        # print(err)
        # 此处可以执行当前会员注册（添加）
        ob = Member()
        ob.nickname = "顾客"  # 默认会员名称
        ob.avatar = "moren.png"  # 默认头像
        ob.mobile = request.POST['mobile']  # 手机号码
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        member = ob
    # 检验当前会员状态
    if member.status == 1:
        # 将当前会员信息转成字典格式并存放到session中
        request.session['mobileuser'] = member.toDict()
        # 重定向到登录页
        return redirect(reverse("mobile_index"))
    else:
        context = {"info": '此账户信息禁用！'}
        return render(request, "mobile/register.html", context)


# 选择店铺
def shop(request):
    context = {'shoplist': Shop.objects.filter(status=1)}
    return render(request, 'mobile/shop.html', context)


# 执行选择店铺
def selectShop(request):
    # 获取店铺信息，放session中
    sid = request.GET['sid']
    ob = Shop.objects.get(id = sid)
    request.session['shopinfo'] = ob.toDict()
    return redirect(reverse("mobile_index"))
# 下单页面
def addOrders(request):
    return render(request, 'mobile/addOrders.html')
