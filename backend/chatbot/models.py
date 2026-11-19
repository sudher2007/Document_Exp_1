import uuid
from django.db import models
from django.utils import timezone

class ChatSession(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.id}"

class Document(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('error', 'Error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20) # pdf, docx, txt
    file_size = models.BigIntegerField(default=0) # in bytes
    page_count = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    error_message = models.TextField(blank=True, default='')
    full_text = models.TextField(blank=True, default='')
    file_path = models.CharField(max_length=512, blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.filename} ({self.status})"

class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField(default=0)
    page_number = models.IntegerField(default=1)
    heading = models.CharField(max_length=255, blank=True, default='')
    text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.filename} (p. {self.page_number})"

class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}..."
