from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def index(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app/login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'app/register.html', {'error': error_message})

    return render(request, 'app/register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('join_room')
        else:
            return render(request, 'app/login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'app/login.html')

def join_room(request):
    return render(request, 'app/join_room.html')

def room(request, room_name):
    response = render(request, "app/room.html", {"room_name": room_name})

    response.set_cookie('user_id', value='12345',samesite='None', secure=True)

    return response
