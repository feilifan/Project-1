from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
def test(request):
	return render_to_response('class_register.html')