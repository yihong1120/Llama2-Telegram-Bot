from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from .models import ChatLog
import os, json
import glob
from django.http import HttpRequest

def home(request: HttpRequest) -> HttpResponse:
    """
    Home view that redirects authenticated users to the dashboard 
    and unauthenticated users to the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return auth_views.LoginView.as_view()(request)

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Login view that redirects authenticated users to the dashboard 
    and unauthenticated users to the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'login.html')

def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logout view that logs out the user and redirects to the homepage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    # Log out the user.
    logout(request)
    # Redirect to the homepage.
    return redirect('/')

def register(request: HttpRequest) -> HttpResponse:
    """
    Registration view that allows unauthenticated users to create a new account.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """
    Profile view that displays the profile of the logged in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    return render(request, 'profile.html')

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Dashboard view that displays the dashboard to the logged in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    # Get all log files
    log_files = [f for f in os.listdir("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs") if f.endswith('.log')]

    # Get all JSON files
    json_files = [f for f in os.listdir("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records") if f.endswith('.json')]

    context = {
        'log_files': log_files,
        'json_files': json_files
    }
    return render(request, 'dashboard.html', context)

@login_required
def download_log_file(request: HttpRequest, log_filename: str) -> HttpResponse:
    """
    View to download a log file.

    Args:
        request (HttpRequest): The request object.
        log_filename (str): The name of the log file to download.

    Returns:
        HttpResponse: The HTTP response.
    """
    log_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs", log_filename)
    if os.path.exists(log_path):
        with open(log_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="text/plain")
            response['Content-Disposition'] = f'attachment; filename={log_filename}'
            return response
    return HttpResponseNotFound("Log file not found.")

@login_required
def view_log_file(request: HttpRequest, log_filename: str) -> HttpResponse:
    """
    View to display the content of a log file.

    Args:
        request (HttpRequest): The request object.
        log_filename (str): The name of the log file to display.

    Returns:
        HttpResponse: The HTTP response.
    """
    log_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs", log_filename)
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            log_content = file.read()
        return render(request, 'log_file_content.html', {'log_content': log_content, 'log_filename': log_filename})
    return HttpResponseNotFound("Log file not found.")

@login_required
def view_json_file(request: HttpRequest, json_filename: str) -> HttpResponse:
    """
    View to display the content of a JSON file.

    Args:
        request (HttpRequest): The request object.
        json_filename (str): The name of the JSON file to display.

    Returns:
        HttpResponse: The HTTP response.
    """
    json_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records", json_filename)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)  # Using json.load to parse the JSON content
        return render(request, 'json_file_content.html', {'json_content': json_content})
    return HttpResponseNotFound("JSON file not found.")

@login_required
def download_json_file(request: HttpRequest, json_filename: str) -> HttpResponse:
    """
    View to download a JSON file.

    Args:
        request (HttpRequest): The request object.
        json_filename (str): The name of the JSON file to download.

    Returns:
        HttpResponse: The HTTP response.
    """
    # Specify the full path of the JSON file
    json_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records", json_filename)

    # Check if the file exists
    if os.path.exists(json_path):
        # Use FileResponse to return the file content
        response = FileResponse(open(json_path, 'rb'), content_type='application/json')
        # Set the response header to tell the browser this is a file to download
        response['Content-Disposition'] = f'attachment; filename="{json_filename}"'
        return response
    else:
        return HttpResponseNotFound("JSON file not found.")
