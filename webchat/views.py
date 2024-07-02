from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from .models import Conversation
from rest_framework.response import Response
from .serializers import MessageSerializer
from .schema import message_list_docs


class MessageViewSet(viewsets.ViewSet):
    @message_list_docs
    def list(self, request):
        channel_id=request.query_params.get("channel_id")
        conversation,_=Conversation.objects.get_or_create(channel_id=channel_id)
        
        message=conversation.messages.all()
        serializer=MessageSerializer(message,many=True)
        return Response(serializer.data)





    pass
