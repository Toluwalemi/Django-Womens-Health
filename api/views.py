# Create your views here.

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.cycle_events import fetch_serialized_data, helper_cycle_event
from api.helpers.helpers import response_helper
from api.models import PeriodCycle
from api.serializers import PeriodCycleSerializer


def ping(request):
    """Health Check"""
    data = {"ping": "pong!"}
    return JsonResponse(data)


class PeriodCycleList(ListCreateAPIView):
    """
    List View to create a period cycle
    """
    queryset = PeriodCycle.objects.all()
    serializer_class = PeriodCycleSerializer

    def post(self, request, *args, **kwargs):
        serializer = PeriodCycleSerializer(data=request.data)
        if serializer.is_valid():
            total_created_cycles = response_helper(serializer)
            return Response({"total_created_cycles": total_created_cycles}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeriodCycleDetail(RetrieveUpdateDestroyAPIView):
    """
    Detail View to update view
    """
    queryset = PeriodCycle.objects.all()
    serializer_class = PeriodCycleSerializer

    def update(self, request, *args, **kwargs):
        instance = PeriodCycle.objects.get(pk=self.kwargs['pk'])
        serializer_class = PeriodCycleSerializer(instance, data=request.data)
        if serializer_class.is_valid():
            total_created_cycles = response_helper(serializer_class)
            return Response({"data": serializer_class.data,
                             "total_created_cycles": total_created_cycles}
                            )

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class CycleEventView(APIView):
    """
    Method to determine what event is happening with respect to requirement 1
    """

    def get(self, request):
        date = request.GET.get('date')
        try:
            queryset = PeriodCycle.objects.get(id=1)
        except queryset.DoesNotExist:
            return Response({"msg": "Object not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PeriodCycleSerializer(queryset)
        queryset_params: dict = fetch_serialized_data(serializer)
        if date:
            return Response(helper_cycle_event(queryset_params, date))

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
