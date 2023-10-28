from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatLog

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
