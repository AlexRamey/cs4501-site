from django.shortcuts import render
from django.shortcuts import render_to_response

def base(request):
	#helloMsg = "Experience Home! API Version: 1"
	return render(request, 'isa_webapp/base.html')#, {'helloMsg' : helloMsg})
