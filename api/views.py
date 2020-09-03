# Drf package
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Custom package
from api.models import ConfirmedCase, District
from api.serializers import ConfirmedCaseSerializer, DistrictSerializer


class CovidityAPIView(APIView):
    def get(self, request):
        # TODO - 지역 이름 받아오기
        # TODO - 지역에 해당하는 확진자 케이스 최근 7일 가져오기
        # TODO - 일 별로 중복되는 ConfirmedCase는 최신 것만 가져오기
        districts = District.objects.all()
        districts_data = DistrictSerializer(districts, many=True).data
        return Response(districts_data)

    def post(self, request):

        return Response(-1)
