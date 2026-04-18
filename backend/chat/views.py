from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import ChatMessage
from .serializers import ChatMessageSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name="session_id", description="Chat session UUID", type=str, required=True),
    ],
)
class ChatHistoryView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        session_id = self.request.query_params.get("session_id", "")
        return ChatMessage.objects.filter(session_id=session_id).order_by("-created_at")[:50]


@extend_schema(
    parameters=[
        OpenApiParameter(name="session_id", description="Chat session UUID", type=str, required=True),
    ],
    responses={204: None},
)
class ClearChatHistoryView(APIView):
    def delete(self, request):
        session_id = request.query_params.get("session_id", "")
        if session_id:
            ChatMessage.objects.filter(session_id=session_id).delete()
        return Response(status=204)
