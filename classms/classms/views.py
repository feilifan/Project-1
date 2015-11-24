from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
def m_apply(request):
	return render_to_response('class_apply.html',)
def binfo(request):
	return render_to_response('class_binfo.html',)
def discuss(request):
	return render_to_response('class_discuss.html',)
def home(request):
	return render_to_response('class_home.html',)
def mainlist(request):
	return render_to_response('class_mainlist.html',)
def register(request):
	return render_to_response('class_register.html',)
def seediscuss(request):
	return render_to_response('class_seediscuss.html',)
def selflist(request):
	return render_to_response('class_selflist.html',)