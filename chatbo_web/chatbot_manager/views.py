from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import ChatLog

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    # Log out the user.
    logout(request)
    # Redirect to the homepage.
    return redirect('/')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def dashboard(request):
    logs = ChatLog.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'logs': logs})

@login_required
def download_log(request, log_id):
    log = ChatLog.objects.get(pk=log_id, user=request.user)
    if log:
        with open(log.log_file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="text/plain")
            response['Content-Disposition'] = f'attachment; filename={log.log_file.name}'
            return response
    return redirect('dashboard')
