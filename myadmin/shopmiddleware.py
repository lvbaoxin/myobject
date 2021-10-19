from django.shortcuts import redirect
from django.urls import reverse
import re


class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # print("url:", path)
        # 判断管理后台是否登录 当前path是否以/myadmin开头，并且不在urllist中，才做是否登录判断
        urllist = ['/myadmin/login', '/myadmin/logout', '/myadmin/dologin', '/myadmin/verify']
        if re.match(r"^/myadmin", path) and (path not in urllist):
            # 判断是否登录(key名为adminuser)
            if 'adminuser' not in request.session:
                # 重定向
                return redirect(reverse("myadmin_login"))

        # 大堂点餐请求的判断，判断是否登录(session中是否有webuser)
        if re.match(r"^/web", path):
            # 判断是否登录(webuser)
            if 'webuser' not in request.session:
                # 重定向
                return redirect(reverse("web_login"))
        # 判断移动端是否登录 当前path是否以/mobile开头，并且不在urllist中，才做是否登录判断
        urllist = ['/mobile/register', '/mobile/doregister']
        if re.match(r"^/mobile", path) and (path not in urllist):
            # 判断是否登录(key名为mobileuser)
            if 'mobileuser' not in request.session:
                # 重定向
                return redirect(reverse("mobile_register"))

        response = self.get_response(request)
        return response
