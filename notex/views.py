from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from user.models import User
from .models import Note

#装饰器
def check_login(fn):

    def wrap(request,*args,**kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username=request.COOKIES.get('username')
            c_uid=request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username']=c_username
                request.session['uid']=c_uid

        return fn(request,*args,**kwargs)
    return wrap



# Create your views here.
@check_login
def add_note(request):
    username=request.COOKIES.get('username')
    if request.method == 'GET':
        return render(request,'notex/add_note.html',locals())

    elif request.method == 'POST':
        user = User.objects.get(username=username)
        title=request.POST['title']
        content=request.POST['content']
        note=Note.objects.create(title=title,content=content,user=user)

        return HttpResponse('添加笔记成功')

def del_note(request):

    return HttpResponseRedirect('删除成功')
    #return HttpResponseRedirect('/index')


def update_note(request):




    return HttpResponseRedirect('/index')


def note_index(request):
    username=request.COOKIES['username']
    uid=request.COOKIES['uid']
    user=User.objects.get(id=uid)
    notes=user.note_set.all()



    return render(request,'notex/note_index.html',locals())


