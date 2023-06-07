from django.shortcuts import render
import urllib.request
import urllib.parse
import json


def index(request):
    return render(request, 'search/search-main.html',)


def result(request):
    player_exist = False
    player_info = {}
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjEzMjU2MTE2MzQiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTcwMTU5Mjk5NCwiaWF0IjoxNjg2MDQwOTk0LCJuYmYiOjE2ODYwNDA5OTQsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.3HWJSkPO9qngikbocORmWwI_fMlPoMMf3pqECltXqkI"
    if request.method == "GET":
        player_name = request.GET.get('search_text')
        print(player_name)
        # encText = urllib.parse.quote("utf-8", format(player_name))
        request_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + player_name
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
                            'input_name': player_name
                        })

    if not player_exist:
        return render(request, 'search/search-result.html',
                {
                    'player_exist': player_exist,
                })
