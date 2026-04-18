from django.urls import path

from .views import ChatHistoryView, ClearChatHistoryView

urlpatterns = [
    path("history/", ChatHistoryView.as_view(), name="chat-history"),
    path("history/clear/", ClearChatHistoryView.as_view(), name="chat-history-clear"),
]
