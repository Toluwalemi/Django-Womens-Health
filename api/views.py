# Create your views here.
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PeriodCycleSerializer


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)


class PeriodCycleView(APIView):
    def post(self, request):
        serializer = PeriodCycleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
