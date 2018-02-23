from rest_framework.views import APIView
from rest_framework.response import Response

class ChatbotView(APIView):
    def get(self, request, format=None):
        resp = {'status': 'success'}
        return Response(resp, status=200)