from django.urls import path
from .views import (
    DocumentUploadView,
    DocumentDetailView,
    DocumentActionsView,
    ChatView,
    ChatHistoryView,
    LoadCollegePolicyView,
    DownloadCollegePolicyView,
    SettingsConfigView
)

urlpatterns = [
    # Documents
    path('documents/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/<uuid:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<uuid:pk>/actions/', DocumentActionsView.as_view(), name='document-actions'),

    # Chat
    path('chat/', ChatView.as_view(), name='chat'),
    path('chat/<str:session_id>/history/', ChatHistoryView.as_view(), name='chat-history'),
    path('chat/<str:session_id>/', ChatHistoryView.as_view(), name='chat-clear'),

    # College Policy built-in PDF
    path('load-policy-pdf/', LoadCollegePolicyView.as_view(), name='load-policy-pdf'),
    path('download-policy-pdf/', DownloadCollegePolicyView.as_view(), name='download-policy-pdf'),

    # Settings
    path('settings/', SettingsConfigView.as_view(), name='settings-config'),
]
