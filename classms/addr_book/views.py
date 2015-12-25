from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context
from addr_book.models import Site_time,People,Classroom,Apply_list,Discuss_list
from django.contrib.auth.models import User
from django.contrib import auth
import datetime
# Create your views here.
from django.http import HttpResponse
def class_apply(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
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
        return render_to_response('class_apply.html',{'room':room[0],'apply_time':get['time'],'applyer':applyer,'admin_code':applyer.admin_code})
    return render_to_response('class_apply.html',{'room':room[0],'apply_time':get['time'],'applyer':applyer,'admin_code':applyer.admin_code})
def class_binfo(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    get = request.GET
    room = Classroom.objects.filter(name=get['room'])
    time_list=[]
    for i in range (0,7):
        tmp_time=datetime.datetime.now()
        time_delta=datetime.timedelta(days=i)
        tmp_time=tmp_time+time_delta
        str_time=tmp_time.strftime('%Y-%m-%d')
        time_list.append(str_time)
    return render_to_response('class_binfo.html',{'room':room[0],'time_list':time_list,'admin_code':person.admin_code})
def class_discuss(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    get = request.GET
    room = Classroom.objects.filter(name = get['room'])
    if request.POST:
        post = request.POST
        if 'point' in post and 'content' in post:
            new_discuss = Discuss_list(discusser=People.objects.get(user=request.user),
                                   point = post['point'],
                                   room = get['room'],
                                   content = post['content'])
            new_discuss.save()
            return HttpResponseRedirect('/class_seediscuss/?room='+get['room'])
    return render_to_response('class_discuss.html',{'room':room[0],'admin_code':person.admin_code},)
def class_home(request):
    if request.POST:
        post=request.POST
        user = auth.authenticate(username=post['name'], password=post['code'])
        if user is not None and user.is_active:
            auth.login(request,user)
            person = People.objects.get(name = post['name'])
            apply_list = Apply_list.objects.filter(applyer = person)
            i=0
            nearest_apply = ''
            for m_apply in apply_list:
                if not m_apply.pasttime:
                    nearest_apply = m_apply
                    break
                i = i + 1
            now_time = Site_time.objects.all()
            if now_time:
                now_site_time = now_time[0]
                last_time = now_site_time.last_time
                tmp_time = datetime.datetime.now()
                str_time = str_time=tmp_time.strftime('%Y-%m-%d')
                i = 0
                while last_time!=str_time:
                    i = i + 1
                    time_delta=datetime.timedelta(days=1)
                    tmp_time=tmp_time+time_delta
                    str_time=tmp_time.strftime('%Y-%m-%d')
                if i>0:
                    num = 6*i
                    now_time.update(last_time=str_time)
                    room_list = Classroom.objects.all()
                    for room in room_list:
                        time_acc = room.time_access
                        time_acc = time_acc + '0'*num
                        time_acc = time_acc[num:]
                        room.update(time_access = time_acc)
            else:
                tmp_time = datetime.datetime.now()
                str_time = str_time=tmp_time.strftime('%Y-%m-%d')
                new_site_time = Site_time(last_time = str_time)
                new_site_time.save()
            return HttpResponseRedirect('/class_selflist/')
        else:
            return render_to_response("class_home.html",{"judge":True})
    return render_to_response('class_home.html',{"judge":True})
def class_mainlist(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    if request.POST:
        post = request.POST
        room_list = Classroom.objects.all()
        if post['building']:
            room_list = room_list.filter(building=post['building'])
        if post['floor']:
            room_list = room_list.filter(floor=post['floor'])
        apply_time = post['selYear'] + '-' + post['selMonth'] + '-' +post['selDay'] +'-'+ post['clock']
        if post['size']:
            room_list = room_list.filter(size=post['size'])
        last_list = [post['building'],post['floor'],post['size']]
        try:
            if post['recommend']:
                m_len = len(room_list)
                person = People.objects.get(user=request.user)
                All_apply = Apply_list.objects.all()
                All_discuss = Discuss_list.objects.all()
                mis_room = room_list[0]
                distent = 10000
                for room in room_list:
                    room_apply = All_apply.filter(room=room.name)
                    apply_self = All_apply.filter(applyer=person)
                    room_discuss = All_discuss.filter(room=room.name)
                    room_apply_self = room_apply.filter(applyer=person)
                    room_discuss_self = room_discuss.filter(discusser=person)
                    g_point = 0.0
                    if len(room_discuss):
                        for discuss in room_discuss:
                            g_point = g_point + float(discuss.point)
                        g_point = g_point/(10*len(room_discuss))
                    l_point = 0.0
                    if len(room_discuss_self):
                        for discuss in room_discuss_self:
                            l_point = l_point + float(discuss.point)
                        l_point = l_point/(10*len(room_discuss_self))
                    self_apply_ratio = 0.0
                    if len(apply_self)>0:
                        self_apply_ratio = len(room_apply_self)*1.0/len(apply_self)
                    global_apply_ratio = 0.0
                    if m_len:
                        global_apply_ratio = len(room_apply)*1.0/m_len
                    m_distent = (g_point-1)*(g_point-1)+(l_point-1)*(l_point-1)
                    m_distent = m_distent + (self_apply_ratio-1)*(self_apply_ratio-1)
                    m_distent = m_distent + (global_apply_ratio-1)*(global_apply_ratio-1)
                    if m_distent < distent:
                        distent = m_distent
                        mis_room = room
                room_list = room_list.filter(name = mis_room.name)
        except:
            room_list = room_list
        return render_to_response('class_mainlist.html',{"room_list":room_list,"apply_time":apply_time,'last_list':last_list,"admin_code":person.admin_code})
    return render_to_response('class_mainlist.html',{"admin_code":person.admin_code})
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
                return render_to_response("class_register.html",{'judge':True})
        else:
            error = Context({'judge':False})
            return render_to_response("class_register.html",error)
    error = Context({'judge':True})
    return render_to_response("class_register.html",error)
def class_admin_register(request):
    if request.POST:
        post = request.POST
        if post['code']==post['codex'] and post['admin_code']=='4d43e8685dc38071':
            nickname =request.POST['name']
            code =request.POST['code']
            try:
                user = User.objects.create_user(username=nickname,password=code)
                user.save()
                new_people = People(user = user,
                                    email= post['email'],
                                    nickname = post['nickname'],
                                    name = post['name'],
                                    school_number = post['id'],
                                    admin_code = True)
                new_people.save()
            except:
                return render_to_response("class_admin_register.html",{'judge':True})
        else:
            error = Context({'judge':False})
            return render_to_response("class_admin_register.html",error)
    error = Context({'judge':True})
    return render_to_response("class_admin_register.html",error)
def class_seediscuss(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    get = request.GET
    room = Classroom.objects.filter(name = get['room'])
    discuss_list = Discuss_list.objects.all()
    return render_to_response('class_seediscuss.html',{'room':room[0],'discuss_list':discuss_list,"admin_code":person.admin_code})
def class_selflist(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    if not person:
        return HttpResponseRedirect('/home/')
    apply_list = Apply_list.objects.filter(applyer = person)
    per_discuss = Discuss_list.objects.filter(discusser = person) 
    flag = False
    now_num = 0
    for m_apply in apply_list:
        if not m_apply.pasttime:
            if m_apply.state=="yes":
                flag = True
                nearest_apply = m_apply
                break
    for m_apply in apply_list:
        if m_apply.state=="yes":
            now_num = now_num+1;
    dic={"person":person,'now_num':now_num,'all_num':len(apply_list),'dis_num':len(per_discuss),'apply_list':apply_list,'admin_code':person.admin_code}
    if flag:
        dic["nearest_apply"]=nearest_apply;
    return render_to_response('class_selflist.html',dic)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/home/')
def class_delete(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    get = request.GET
    apply_item = Apply_list.objects.get(room=get['room'],time=get['time'])
    apply_item.delete()
    person = People.objects.get(name = request.user.username)
    apply_list = Apply_list.objects.filter(applyer = person)
    i=0
    dic={"person":person,'apply_list':apply_list,"admin_code":person.admin_code}
    for m_apply in apply_list:
        if not m_apply.pasttime:
            nearest_apply = m_apply
            dic['nearest_apply']=nearest_apply
            break
        i = i + 1
    return render_to_response('class_selflist.html',dic)
def class_admin(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    if person.admin_code==False:
        return HttpResponseRedirect('/home/')
    if request.POST:
        post = request.POST
        hoster = People.objects.get(name = request.user.username)
        new_room = Classroom(hoster = hoster,
                             name = post['name'],
                             floor = post['floor'],
                             building = post['building'],
                             size = post['size'],
                             time_access = "0"*42)
        new_room.save()
        return render_to_response("demo.html")
    return render_to_response("demo.html")

def class_deal(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    if person.admin_code==False:
        return HttpResponseRedirect('/home/')
    apply_list = Apply_list.objects.filter(state = 'notyet')
    apply_list = apply_list.order_by('-time')
    return render_to_response('demo2.html',{'apply_list':apply_list})
    
def class_deal_true(request):
    if not request.user.username:
        return HttpResponseRedirect('/home/')
    person = People.objects.get(name = request.user.username)
    if person.admin_code==False:
        return HttpResponseRedirect('/home/')
    get = request.GET
    applyer = People.objects.filter(name=get['applyer'])
    m_apply = Apply_list.objects.filter(room=get['room'],time=get['time'],applyer=applyer[0])
    if request.POST:
        post = request.POST
        if post['yes']:
            m_apply.update(state="yes")
            m_plz = 0
            for i in range (0,7):
                tmp_time=datetime.datetime.now()
                time_delta=datetime.timedelta(days=i)
                tmp_time=tmp_time+time_delta
                str_time=tmp_time.strftime('%Y-%m-%d')
                if str_time == m_apply[0].time[0:10]:
                    if m_apply[0].time[10:22]=="-08:00-09:45":
                        m_plz = i*6
                    elif m_apply[0].time[10:22] =="-10:00-11:45":
                        m_plz = i*6+1
                    elif m_apply[0].time[10:22]=="-13:45-15:30":
                        m_plz = i*6+2
                    elif m_apply[0].time[10:22]=="-15:45-17:30":
                        m_plz = i*6+3
                    elif m_apply[0].time[10:22]=="-18:30-21:10":
                        m_plz = i*6+4
                    elif m_apply[0].time[10:22]=="-21:20-22:50":
                        m_plz = i*6+5
            m_room = Classroom.objects.filter(name = get['room'])
            old_time = m_room[0].time_access
            new_time = old_time[0:m_plz]+'1'+old_time[m_plz+1:42]
            m_room.update(time_access=new_time)
        else:
            m_apply.update(state="no")
    return render_to_response("demo3.html",{'m_apply':m_apply[0]})
        
        
    
            