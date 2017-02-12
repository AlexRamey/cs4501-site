from django.shortcuts import render

def index(request):
	helloMsg = "Models Home!"
	return render(request, 'isa_models/index.html', {'helloMsg' : helloMsg})