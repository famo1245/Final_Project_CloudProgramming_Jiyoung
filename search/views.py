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
        print(player_name)
        # 한국어 닉네임의 경우 ascii로 변환해줘야 함
        enc_name = urllib.parse.quote(player_name)
        request_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + enc_name
        api_request = urllib.request.Request(request_url)
        api_request.add_header("Authorization", api_key)
        response = urllib.request.urlopen(api_request)
        res_code = response.getcode()

        if res_code == 200:
            print('ok')
            response_body = response.read()
            player_result = json.loads(response_body.decode('utf-8'))
            player_exist = True

            if player_exist:
                player_info['nickname'] = player_result['nickname']
                player_info['level'] = player_result['level']

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
