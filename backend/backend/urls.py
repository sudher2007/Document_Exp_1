from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
from pathlib import Path

def serve_frontend(request):
    index_file = settings.FRONTEND_DIR / 'index.html'
    if index_file.exists():
        return FileResponse(open(index_file, 'rb'), content_type='text/html')
    return HttpResponse(
        "<h1>Document GroundQ&A API Running</h1><p>Frontend is building or running at http://localhost:5173</p>",
        content_type='text/html'
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),
    path('', serve_frontend, name='frontend-root'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.FRONTEND_DIR / 'assets')
