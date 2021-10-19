from django.urls import path
from mobile.views import index, member

urlpatterns = [
    path('', index.index, name="mobile_index"),
    path('register', index.register, name="mobile_register"),
    path('doregister', index.doRegister, name="mobile_doregister"),
    path('shop', index.shop, name="mobile_shop"),
    path('shop/select', index.selectShop, name="mobile_selectshop"),
    path('orders/add', index.addOrders, name="mobile_addorders"),
    path('member', member.index, name="mobile_member_index"),
    path('member/orders', member.orders, name="mobile_member_orders"),
    path('member/detail', member.detail, name="mobile_member_detail"),
    path('member/logout', member.logout, name="mobile_member_logout"),

]
