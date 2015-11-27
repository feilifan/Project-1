#coding=utf-8
from django.shortcuts import render, render_to_response
from django.template import Context
from addr_book.models import People,Classroom,Apply_list,Discuss_list
from django.contrib.auth.models import User
from django.contrib import auth
import re
# Create your views here.
from django.http import HttpResponse
def class_apply(request):
    if not request.user:
        return render_to_response('class_home.html')
    get = request.GET
    room = Classroom.objects.filter(name=get['room'])
    applyer = People.objects.get(user = request.user)
    if request.POST:
        post = request.POST
        new_apply = Apply_list(applyer=applyer,
                               time=get['time'],
                               hostname=room[0].hoster.name,
                               room=room[0].name,
                               state='notyet',
                               reason=post['reason'])
        new_apply.save()
        return render_to_response('class_apply.html',{'room':room[0],'apply_time':get['time'],'applyer':applyer})
    return render_to_response('class_apply.html',{'room':room[0],'apply_time':get['time'],'applyer':applyer})
def class_binfo(request):
    if not request.user:
        return render_to_response('class_home.html')
    return render_to_response('class_binfo.html')
def class_discuss(request):
    if not request.user:
        return render_to_response('class_home.html')
    get = request.GET
    room = Classroom.objects.filter(name = get['room'])
    if request.POST:
        post = request.POST
        new_discuss = Discuss_list(discusser=People.objects.get(user=request.user),
                                   point = get['point'],
                                   content = post['content'])
        new_discuss.save()
        return render_to_response('class_discuss.html',{'room':room[0]})
    return render_to_response('class_discuss.html',{'room':room[0]})
def class_home(request):
    if request.POST:
        post=request.POST
        user = auth.authenticate(username=post['name'], password=post['code'])
        if user is not None and user.is_active:
            auth.login(request,user)
            person = People.objects.get(name = post['name'])
            apply_list = Apply_list.objects.filter(applyer = person)
            return render_to_response("class_selflist.html",{"person":person,"apply_list":apply_list})
        else:
            return render_to_response("class_home.html",{"judge":True})
    return render_to_response('class_home.html',{"judge":True})
def class_mainlist(request):
    if not request.user:
        return render_to_response('class_home.html')
    if request.POST:
        post = request.POST
        room_list = Classroom.objects.all()
        apply_time = post['selYear'] + '-' + post['selMonth'] + '-' +post['selDay'] +'-'+ post['clock']
        return render_to_response('class_mainlist.html',{"room_list":room_list,"apply_time":apply_time})
    return render_to_response('class_mainlist.html')
def class_register(request):
    if request.POST:
        post = request.POST
        if post['code']==post['codex']:
            nickname =request.POST['name']
            code =request.POST['code']
            try:
                user = User.objects.create_user(username=nickname,password=code)
                user.save()
                new_people = People(user = user,
                                    email= post['email'],
                                    nickname = post['nickname'],
                                    name = post['name'],
                                    school_number = post['id'])
                new_people.save()
            except:
                return render_to_response("class_register.html",{'judge':True,'judge2':False,})
        else:
            error = Context({'judge':False,'judge2':True,})
            return render_to_response("class_register.html",error)
    error = Context({'judge':False,'judge2':True,})
    return render_to_response("class_register.html",error)
def class_seediscuss(request):
    if not request.user:
        return render_to_response('class_home.html')
    get = request.GET
    room = Classroom.objects.filter(name = get['room'])
    discuss_list = Discuss_list.objects.all()
    return render_to_response('class_seediscuss.html',{'room':room[0],'discuss_list':discuss_list})
def class_selflist(request):
    if not request.user:
        return render_to_response('class_home.html')
    person = People.objects.get(name = request.user.username)
    apply_list = Apply_list.objects.filter(applyer = person)
    i=0
    for m_apply in apply_list:
        if not m_apply.pasttime:
            nearest_apply = m_apply
            break
        i = i + 1
    return render_to_response('class_selflist.html',{"person":person,'apply_list':apply_list,'nearest_apply':nearest_apply})
    
def class_delete(request):
    if not request.user:
        return render_to_response('class_home.html')
    get = request.GET
    apply_item = Apply_list.objects.get(room=get['room'],time=get['time'])
    apply_item.delete()
    person = People.objects.get(name = request.user.username)
    apply_list = Apply_list.objects.filter(applyer = person)
    i=0
    for m_apply in apply_list:
        if not m_apply.pasttime:
            nearest_apply = m_apply
            break
        i = i + 1
    return render_to_response('class_selflist.html',{"person":person,'apply_list':apply_list,'nearest_apply':nearest_apply})
def class_admin(request):
    sizelist = ['10-30', '30-50', '50-100', '100-200', '200以上']
    if request.POST:
        #print 'post'
        post = request.POST
        #print request.POST['multimedia']
        hoster = People.objects.get(name = request.user.username)
        new_room = Classroom(hoster = hoster,
                             name = post['name'],
                             floor = post['floor'],
                             building = post['building'],
                             size = post['size'],
                             multimedia = bool(request.POST['multimedia']),
                             time_access = request.POST['time_access'])
        new_room.save()
        #print request.POST['multimedia']
        return render_to_response("demo.html", {'sizelist':sizelist})
    return render_to_response("demo.html", {'sizelist':sizelist})

def class_check(request):
    classlist = Apply_list.objects.filter(state='notyet')
    content = {'classlist': classlist}
    if request.POST:
        #print 'postssssssssssssssssssssssssssssss'
        post = request.POST
        for key in post:
            print key
            applyer = People.objects.filter(name=key)
            app = Apply_list.objects.filter(applyer=applyer)
            print type(post[key]), bool(post[key]) == True, bool(post[key])
            if bool(post[key]) == True:
                state = 'yes'
            else:
                state = 'no'
            print state
            app[0].app(state)
            print app[0].state
        return render(request, "class_check.html", content)
    return render(request, "class_check.html", content)
