from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import Member, Shop, Category, Product, Orders, Payment, OrderDetail


# 首页
def index(request):
    # 获取当前店铺信息
    shopinfo = request.session.get("shopinfo", None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))
    # 获取当前店铺下的菜品类别和信息
    clist = Category.objects.filter(shop_id=shopinfo['id'], status=1)
    productlist = dict()
    for vo in clist:
        plist = Product.objects.filter(category_id=vo.id, status=1)
        productlist[vo.id] = plist
    context = {'categorylist': clist, 'productlist': productlist.items(), 'cid': clist[0]}
    return render(request, 'mobile/index.html', context)


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
    ob = Shop.objects.get(id=sid)
    request.session['shopinfo'] = ob.toDict()
    request.session['cartlist'] = {}
    return redirect(reverse("mobile_index"))


# 下单页面
def addOrders(request):
    # 尝试从session中获取名字为cartlist的购物车信息
    cartlist = request.session.get("cartlist", {})
    total_money = 0
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']

    request.session['total_money'] = total_money
    return render(request, 'mobile/addOrders.html')


def doAddOrders(request):
    '''执行订单添加操作'''
    try:
        # 执行订单信息添加操作
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']  # 店铺id号
        od.member_id = request.session['mobileuser']['id']  # 操作员id
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1  # 订单状态:1过行中/2无效/3已完成
        od.payment_status = 2  # 支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 执行支付信息添加
        op = Payment()
        op.order_id = od.id  # 订单id号
        op.member_id = request.session['mobileuser']['id']  # 操作员id
        op.money = request.session['total_money']  # 支付款
        op.type = 2  # 付款方式：1会员付款/2收银收款
        op.bank = request.GET.get("bank", 3)  # 收款银行渠道:1微信/2余额/3现金/4支付宝
        op.status = 2  # 支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 执行订单详情添加
        cartlist = request.session.get('cartlist', {})
        for shop in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = shop['id']
            ov.product_name = shop['name']
            ov.price = shop['price']
            ov.quantity = shop['num']
            ov.status = 1
            ov.save()
        del request.session['cartlist']
        del request.session['total_money']

    except Exception as err:
        print(err)
    return render(request, 'mobile/orderInfo.html', {'order': od})
