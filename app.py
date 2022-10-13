from flask import Flask, request, jsonify, session
from googleapiclient.discovery import build
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app,supports_credentials=True)

@app.route('/data', methods=['POST'])
def get_channel_stats():
    # youtube
    channel_id = request.json['youtube_id']
    youtube_api_key = 'AIzaSyDk5EXbBMLdZJ5Crd916eN-BYF27YQ3mMU'
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    req = youtube.channels().list(part='statistics', id=channel_id)
    res = req.execute()
    # subscriberCount vs viewCount
    youtube_data = res['items'][0]['statistics']['subscriberCount']
    # twitter
    user_id = request.json['twitter_id']
    url = "https://twitter135.p.rapidapi.com/UserByRestId/"
    querystring = {"id": user_id}
    headers = {
        "X-RapidAPI-Key": "958d53532bmshefb361db40eea45p164fd2jsn0c8ded881732",
        "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    res_j = response.json()
    # total_favorited vs follower_count
    twitter_data = res_j['data']['user']['result']['legacy']['followers_count']
    # tiktok
    username = request.json['tiktok_username']
    url = "https://tiktok_solutions.p.rapidapi.com/user/{}".format(username)
    headers = {
        "X-RapidAPI-Key": "958d53532bmshefb361db40eea45p164fd2jsn0c8ded881732",
        "X-RapidAPI-Host": "tiktok_solutions.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    res_j = response.json()
    # total_favorited vs follower_count
    tiktok_data = res_j['data']['follower_count']
    # instagram
    username = request.json['instargram_username']
    url = "https://instagram130.p.rapidapi.com/account-info"
    querystring = {"username": username}
    headers = {
        "X-RapidAPI-Key": "958d53532bmshefb361db40eea45p164fd2jsn0c8ded881732",
        "X-RapidAPI-Host": "instagram130.p.rapidapi.com"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    res_j = response.json()
    ins_data = res_j['edge_follow']['count']
    total_data = (int(youtube_data)+int(ins_data) +
                  int(twitter_data)+int(tiktok_data))/4
    return jsonify({'data': int(total_data)})


if __name__ == "__main__":
    app.run(debug=True)
