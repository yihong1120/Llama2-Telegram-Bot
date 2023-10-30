from django.db import models
from django.contrib.auth.models import User

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_file = models.FileField(upload_to='logs/')
    json_file = models.FileField(upload_to='chat_records/')
