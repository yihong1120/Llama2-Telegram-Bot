from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from .models import ChatLog
import os, json
import glob

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

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
    # 獲取所有 log 檔案
    log_files = [f for f in os.listdir("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs") if f.endswith('.log')]

    # 獲取所有 JSON 檔案
    json_files = [f for f in os.listdir("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records") if f.endswith('.json')]

    context = {
        'log_files': log_files,
        'json_files': json_files
    }
    return render(request, 'dashboard.html', context)

@login_required
def download_log_file(request, log_filename):
    log_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs", log_filename)
    if os.path.exists(log_path):
        with open(log_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="text/plain")
            response['Content-Disposition'] = f'attachment; filename={log_filename}'
            return response
    return HttpResponseNotFound("Log file not found.")

@login_required
def view_log_file(request, log_filename):
    log_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/logs", log_filename)
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            log_content = file.read()
        return render(request, 'log_file_content.html', {'log_content': log_content, 'log_filename': log_filename})
    return HttpResponseNotFound("Log file not found.")

@login_required
def view_json_file(request, json_filename):
    json_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records", json_filename)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)  # Using json.load to parse the JSON content
        return render(request, 'json_file_content.html', {'json_content': json_content})
    return HttpResponseNotFound("JSON file not found.")


@login_required
def download_json_file(request, json_filename):
    # 指定 JSON 檔案的完整路徑
    json_path = os.path.join("/Users/YiHung/Documents/Side_Projects/Llama2-Telegram-Bot/chat_records", json_filename)

    # 檢查文件是否存在
    if os.path.exists(json_path):
        # 使用 FileResponse 回傳檔案內容
        response = FileResponse(open(json_path, 'rb'), content_type='application/json')
        # 設定回傳的檔頭，告訴瀏覽器這是一個要下載的文件
        response['Content-Disposition'] = f'attachment; filename="{json_filename}"'
        return response
    else:
        return HttpResponseNotFound("JSON file not found.")