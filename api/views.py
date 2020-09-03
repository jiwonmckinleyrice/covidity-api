# Standard package
from datetime import datetime, timedelta
# Django
from django.db.models.functions import TruncDay
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
        district = request.query_params.get('district')
        # TODO - district validation (empty, invalid)
        # 해당 지역에 속한 24시간 내에 가장 이른 케이스와 가장 늦은 케이스 조회
        yesterday_case = ConfirmedCase.objects.filter(
            district__name=district, created_at__gte=datetime.today()-timedelta(days=1)).first()
        today_case = ConfirmedCase.objects.filter(
            district__name=district, created_at__gte=datetime.today()-timedelta(days=1)).last()
        # 질본, 서울시 업데이트 인터벌에 맞춰서 조회 후 직렬화
        data = {
            "yesterday": ConfirmedCaseSerializer(yesterday_case).data,
            "today": ConfirmedCaseSerializer(today_case).data
        }
        return Response(data)

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
            district_object, created = District.objects.get_or_create(
                name=district_name)
            # 지역구 별 확진자 수 갱신 및 등록
            number = numbers[index].get()
            ConfirmedCase.objects.create(
                count=int(number), district=district_object)
            # API Respose 오브젝트 키 추가
            data[district_name] = number
        return Response(data)
