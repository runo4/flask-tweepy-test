import config # twitterAPI credential
import os
import json
import sys
import tweepy
from flask import Flask, session, redirect, render_template, request
from os.path import join, dirname
# from dotenv import load_dotenv 実装予定

#---------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'hogehoge'

#---------------------------------------------------------------------

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET

#---------------------------------------------------------------------

@app.route('/')
def index():
    timeline = get_user_timeline()
    return render_template("index.html", timeline=timeline)

@app.route('/twitter_auth', methods=['GET'])
def twitter_auth():
    redirect_url = ""
    # OAuth認証
    auth = tweepy.OAuthHandler(CK, CS)
    try:
        # 認証用URL取得
        redirect_url = auth.get_authorization_url()
        # セッションにrequest_tokenを保存
        session['request_token'] = auth.request_token
    except Exception as e:
        print(e)

    return redirect(redirect_url)

#---------------------------------------------------------------------

def get_user_timeline():
    if 'request_token' in session:
        print("request_token exist")
    token = session.pop('request_token', None)
    verifier = request.args.get('oauth_verifier')
    if token is None or verifier is None:
        return False # 未認証
    
    # OAuth認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except Exception as e:
        print(e)

    api = tweepy.API(auth)
    return api.user_timeline(count=20)

#---------------------------------------------------------------------

if __name__ == "__main__":
    app.run()