from django.shortcuts import render


def index(request):
	return render(request, 'employer/index.html')

# Create your views here.
