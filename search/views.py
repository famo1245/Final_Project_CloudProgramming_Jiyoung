from django.shortcuts import render
from django.conf import settings
import urllib.request
import urllib.parse
import json


def index(request):
    return render(request, 'search/search-main.html', )


def result(request):
    player_exist = False
    player_info = {}
    api_key = settings.NEXON_KEY
    if request.method == "GET":
        player_name = request.GET.get('search_text')

        # 한국어 닉네임의 경우 ascii로 변환해줘야 함
        enc_name = urllib.parse.quote(player_name)
        request_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + enc_name
        api_request = urllib.request.Request(request_url)
        api_request.add_header("Authorization", api_key)
        response = urllib.request.urlopen(api_request)
        res_code = response.getcode()

        if res_code == 200:
            response_body = response.read()
            player_result = json.loads(response_body.decode('utf-8'))

            if 'accessId' in player_result:
                player_exist = True

            if player_exist:
                player_info['nickname'] = player_result['nickname']
                player_info['level'] = player_result['level']
                access_id = player_result['accessId']

                info_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users/{}/maxdivision".format(access_id)
                info_request = urllib.request.Request(info_url)
                info_request.add_header("Authorization", api_key)
                info_result = urllib.request.urlopen(info_request)
                info_res = info_result.getcode()
                player_info['division'] = '랭크 정보 없음'

                if info_res == 200:
                    info_body = info_result.read()
                    info_result = json.loads(info_body.decode('utf-8'))
                    if info_result:
                        player_info['division'] = convert_division(info_result[0]['division'])

            return render(request, 'search/search-result.html',
                          {
                              'player_exist': player_exist,
                              'player_info': player_info,
                              'player_name': player_name
                          })
    if not player_exist:
        return render(request, 'search/search-result.html',
                      {
                          'player_exist': player_exist,
                      })


def convert_division(division):
    tier = ''
    if division == 800:
        tier = '슈퍼챔피언스'
    elif division == 900:
        tier = '챔피언스'
    elif division == 1000:
        tier = '슈퍼챌린지'
    elif division == 1100:
        tier = '챌린지1'
    elif division == 1200:
        tier = '챌린지2'
    elif division == 1300:
        tier = '챌린지3'
    elif division == 2000:
        tier = '월드클래스1'
    elif division == 2100:
        tier = '월드클래스2'
    elif division == 2200:
        tier = '월드클래스3'
    elif division == 2300:
        tier = '프로1'
    elif division == 2400:
        tier = '프로2'
    elif division == 2500:
        tier = '프로3'
    elif division == 2600:
        tier = '세미프로1'
    elif division == 2700:
        tier = '세미프로2'
    elif division == 2800:
        tier = '세미프로3'
    elif division == 2900:
        tier = '유망주1'
    elif division == 3000:
        tier = '유망주2'
    elif division == 3100:
        tier = '유망주3'

    return tier
