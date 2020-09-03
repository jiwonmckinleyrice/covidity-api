# Drf package
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Third-party package
import requests
from scrapy.selector import Selector
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
        data = {}
        html = requests.get("http://www.seoul.go.kr/coronaV/coronaStatus.do")
        selector = Selector(text=html.text)
        districts = selector.xpath(
            '//table[@class="tstyle-status pc pc-table"]/tbody/tr/th/text()')
        numbers = selector.xpath(
            '//table[@class="tstyle-status pc pc-table"]/tbody/tr/td/text()')
        for index, district in enumerate(districts):
            # 지역구 데이터베이스 초기화 혹은 등록
            district_name = district.get()
            district_object, created = District.objects.get_or_create(name=district_name)
            # 지역구 별 확진자 수 갱신 및 등록
            number = numbers[index].get()
            ConfirmedCase.objects.create(count=int(number), district=district_object)
            # API Respose 오브젝트 키 추가
            data[district_name] = number
        return Response(data)
