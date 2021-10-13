from django.urls import path, include
from web.views import index

urlpatterns = [
    path('', index.index, name="index"),
    path('login', index.login, name="web_login"),  # 加载登录表单
    path('dologin', index.dologin, name="web_dologin"),  # 执行登录表单
    path('logout', index.logout, name="web_logout"),  # 退出登录
    path('verify', index.verify, name="web_verify"),  # 验证码
    #  为url路由加web/
    path('web/', include([
        path('', index.webindex, name="web_index")  # 前台大堂点菜
    ]))
]
