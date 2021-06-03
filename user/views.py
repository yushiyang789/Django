import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User

# Create your views here.
def reg_view(request):

    #注册
    if request.method == 'GET':
        # GET返回页面
        return render(request,'user/register.html')
    elif request.method == 'POST':
        # POST处理提交数据
        username=request.POST['username']
        password_1=request.POST['password_1']
        password_2 = request.POST['password_2']

        # 1 两次密码一致
        if password_1 != password_2:
            return HttpResponse('两次密码输入不一致')

    #哈希算法 - 给定明文，计算出一段定长的，不可逆的值
    #md5 特点
    #1 定长输入：不管明文输入长度为多少，哈希值都是定长的，md5-32位16进制
    #2 不可逆：无法反向计算出 对应的 明文
    #3 雪崩效应：输入改变，输出必然变
    #场景：1，密码处理 2，文件完整性验证
    m=hashlib.md5()
    m.update(password_1.encode())
    password_m=m.hexdigest()

    #2 用户名是否已经注册
    old_users=User.objects.filter(username=username)
    if old_users:
        return HttpResponse('用户名已注册')
    #3 插入数据
    try:
        user=User.objects.create(username=username,password=password_m)
    except Exception as e:
        print(e)
        return HttpResponse('用户名已注册')
    request.session['username']=username
    request.session['uid']=user.id


    return HttpResponseRedirect('/index')


def login_view(request):

    if request.method == 'GET':
        #获取登录页面
        #检查登录状态，如果登录了，显示已登录
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        #检查cookies
        c_username=request.COOKIES.get('username')
        c_uid=request.COOKIES.get('uid')
        if c_username and c_uid:
            #回写session
            request.session['username']=c_username
            request.session['uid']=c_uid
            return HttpResponseRedirect('/index')

        return render(request,'user/login.html')

    elif request.method == 'POST':
        #处理数据
        username=request.POST['username']
        password=request.POST['password']

        try:
            user=User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s'%(e))
            return HttpResponse('用户名或密码错误')
        m = hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码错误')
        #记录会话状态

        request.session['username']=username
        request.session['uid']=user.id

        resp=HttpResponseRedirect('/index')
        #判断用户是否勾选了记住用户名
        if 'remember' in request.POST:
        #如果勾选了，则设置Cookies
            resp.set_cookie('uid',user.id,3600*24*3)
            resp.set_cookie('username',username,3600*24*3)


        return resp

def logout_view(request):
    resq=HttpResponseRedirect('/index')
    resq.delete_cookie('username')
    resq.delete_cookie('uid')

    if request.session.get('username') and request.session.get('uid'):
        del request.session['uid']
        del request.session['username']

    return resq

