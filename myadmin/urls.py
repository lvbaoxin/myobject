from django.urls import path
from myadmin.views import index
from myadmin.views import user

urlpatterns = [
    path('', index.index, name="myadmin_index"),
    # 员工信息路由
    path('user/<int:pIndex>', user.index, name="myadmin_user_index"),  # 浏览
    path('user/add', user.add, name="myadmin_user_add"),  # 添加表单
    path('user/insert', user.insert, name="myadmin_user_insert"),  # 执行添加
    path('user/del<int:uid>', user.delete, name="myadmin_user_delete"),  # 执行删除
    path('user/edit<int:uid>', user.edit, name="myadmin_user_edit"),  # 编辑表单
    path('user/update<int:uid>', user.update, name="myadmin_user_update"),  # 执行编辑
    path('login', index.login, name="myadmin_login"),  # 加载登录表单
    path('dologin', index.dologin, name="myadmin_dologin"),  # 执行登录表单
    path('logout', index.logout, name="myadmin_logout"),  #  退出登录
    path('verify', index.verify, name="myadmin_verify"),  #  验证码
]
