# Create your views here.
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers import fetch_serialized_data, calculate_no_of_days, calculate_total_created_cycle
from api.serializers import PeriodCycleSerializer


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)


class PeriodCycleView(APIView):
    def post(self, request):
        serializer = PeriodCycleSerializer(data=request.data)

        if serializer.is_valid():
            serialized_data = fetch_serialized_data(serializer)
            get_difference = calculate_no_of_days(serialized_data["start_date"], serialized_data["end_date"])
            total_created_cycles = calculate_total_created_cycle(serialized_data["cycle_average"], get_difference)
            serializer.save()

            return Response({"total_created_cycles": total_created_cycles}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
