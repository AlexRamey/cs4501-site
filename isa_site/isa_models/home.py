from django.shortcuts import render

def index(request):
	helloMsg = "Models Home! API Version: 1"
	return render(request, 'isa_models/index.html', {'helloMsg' : helloMsg})