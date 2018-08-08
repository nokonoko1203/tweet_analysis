#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tweepyライブラリをインポート
import tweepy
import os


# 各種キーをセット
CONSUMER_KEY_2 = os.environ.get('CONSUMER_KEY_2')
CONSUMER_SECRET_2 = os.environ.get("CONSUMER_SECRET_2")
ACCESS_TOKEN_2 = os.environ.get("ACCESS_TOKEN_2")
ACCESS_SECRET_2 = os.environ.get("ACCESS_SECRET_2")
auth = tweepy.OAuthHandler(CONSUMER_KEY_2, CONSUMER_SECRET_2)
auth.set_access_token(ACCESS_TOKEN_2, ACCESS_SECRET_2)
#APIインスタンスを作成
api = tweepy.API(auth)
