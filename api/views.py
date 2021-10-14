# Create your views here.
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers import fetch_serialized_data, calculate_no_of_days, calculate_total_created_cycle, response_helper
from api.models import PeriodCycle
from api.serializers import PeriodCycleSerializer


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)


class PeriodCycleView(APIView):
    def post(self, request):
        serializer = PeriodCycleSerializer(data=request.data)
        if serializer.is_valid():
            total_created_cycles = response_helper(serializer)
            return Response({"total_created_cycles": total_created_cycles}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeriodCycleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PeriodCycle.objects.all()
    serializer_class = PeriodCycleSerializer

    def update(self, request, *args, **kwargs):
        instance = PeriodCycle.objects.get(pk=self.kwargs['pk'])
        serializer_class = PeriodCycleSerializer(instance, data=request.data)
        if serializer_class.is_valid():
            total_created_cycles = response_helper(serializer_class)
            return Response(
                {"data": serializer_class.data,
                 "total_created_cycles": total_created_cycles
                 }, status=status.HTTP_200_OK
            )

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
