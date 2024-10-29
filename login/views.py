from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .form import LoginForm, RegisterForm
from django.contrib import messages
def home(request: HttpRequest):
    return render(request, "try_bootstrap.html")
# Create your views here.

def bootstrap(request: HttpRequest):
    return render(request, "try_bootstrap5.html")

# def login(request: HttpRequest):
#     if request.session.get("is_login", None):
#         return redirect("/dashboard/")
#
#     if request.method == "GET":
#         return render(request, "login.html")
#
#     if request.method == "POST":
#         # print(request.POST)
#         login_form = LoginForm(request.POST)
#         register_form = RegisterForm(request.POST)
#
#         if login_form.is_valid():
#             username = login_form.cleaned_data["log_username"]
#             password = login_form.cleaned_data["log_password"]
#             # print(username, password)
#             login_result = 1
#             #login(username, password)
#
#             if login_result == 0:
#                 request.session["is_login"] = True
#                 request.session["user_name"] = username
#                 return redirect("/dashboard/")
#             elif login_result == 1:
#                 messages.error(request, "密码错误！")
#             elif login_result == -1:
#                 messages.error(request, "用户不存在！")
#
#             return render(request, "login.html", locals())
#
#         elif register_form.is_valid():
#             username = register_form.cleaned_data["reg_username"]
#             email = register_form.cleaned_data["reg_email"]
#             password = register_form.cleaned_data["reg_password"]
#             password2 = register_form.cleaned_data["reg_password2"]
#
#             reg_result =  0
#             # register(username, password)
#
#             if reg_result == 0:
#                 messages.success(request, "注册成功！")
#                 return redirect("/login/")
#             elif reg_result == 1:
#                 messages.error(request, "用户已存在！")
#
#             return render(request, "login.html", locals())
#
#         return render(request, "try_bootstrap.html", locals())

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User


def login(request):
    if request.session.get("is_login", None):
        return redirect("/dashboard/")

    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        # 提取表单数据
        username = request.POST.get("name")
        password = request.POST.get("password")
        action = request.POST.get("action")  # 区分登录和注册

        if action == "login":
            # 登录逻辑
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session["is_login"] = True
                request.session["user_name"] = username
                auth_login(request, user)
                return redirect("/dashboard/")
            else:
                messages.error(request, "用户名或密码错误！")

        elif action == "register":
            # 注册逻辑
            # email = request.POST.get("email")
            password2 = request.POST.get("confirm_password")  # 确认密码字段

            if password == password2:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    messages.success(request, "注册成功！请登录。")
                    return redirect("/login/")
                except Exception as e:
                    messages.error(request, "注册失败：" + str(e))
            else:
                messages.error(request, "密码不匹配！")

    return render(request, "login.html")
