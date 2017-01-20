#from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	helloMsg = "Hello World! Welcome Home And Happy New Year! :)"
	return render(request, 'ramey/index.html', {'helloMsg' : helloMsg})
	