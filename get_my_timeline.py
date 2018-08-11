# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Tweepyライブラリをインポート
import tweepy
import auth
api = auth.api
import get_fav
import os
import datetime
import pandas as pd
import matplotlib
# cloud9では以下を指定しないとエラーがでる
matplotlib.use('Agg')
# 上記記述後に「.pyplot」をimportすること
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))

# チャートがきれいに書けるおまじない
plt.style.use('ggplot') 
font = {'family' : 'meiryo'}
matplotlib.rc('font', **font)


# 指定されたユーザーのツイートのタイムラインjsonで取得？
user_name = "nokonoko_1203"
# 現在の日時と30日前の日時を取得
now = datetime.datetime.now()
delta = datetime.timedelta(days=-30)
one_month_ago = now + delta
# 自分のツイートを複数件取得(MAXで1000件)
my_tweet = tweepy.Cursor(api.user_timeline, screen_name=user_name).items(1000)
                        
#「api.user_timeline」ではsinceとuntilは指定出来ない
# my_tweet = tweepy.Cursor(api.user_timeline, screen_name=user_name, 
#                         since=one_month_ago.strftime('%Y-%m-%d'),
#                         until=now.strftime('%Y-%m-%d')).items()

def get_my_timeline(my_tweet):
    status_count = 0
    fav_count_list = []
    retweet_count_list = []
    # 各ツイートに分解
    for status in my_tweet:
        # いいねが１以上ついていて、メンションじゃないツイートを取得
        if status.favorite_count >= 1 and "@" not in status.text:
            # ツイートの内容を取得
            text = status.text
            # いいね数を取得
            fav_count = status.favorite_count
            fav_count_list.append(fav_count)
            # リツイート数を取得
            retweet_count = status.retweet_count
            retweet_count_list.append(retweet_count)
            # いいねされたツイートのidからアカウントのidを検索
            tweet_fav_id = get_fav.get_favoritters(status.id)
            for fav_menber_id in tweet_fav_id:
                # idからアカウント名を検索
                user = api.get_user(user_id=fav_menber_id).screen_name
                # ツイートの情報には自分の情報も入っているのでスルーする
                if user == "nokonoko_1203":
                    continue
                # フォロワー数を表示
                follower_count = api.get_user(user_id=fav_menber_id).followers_count

            # 投稿時間を取得して、日本時間に変換（９時間を足す）
            ja_datetime = status.created_at + datetime.timedelta(hours=9)
            status_count += 1
            # 最新20件のみ取得
            if status_count == 20:
                print("取得完了")
                break
     
   
# １ヶ月分の投稿を取得して、投稿ごとの「いいね数・リツイート数・投稿時間」を返す
def get_my_tweet_one_month(my_tweet):
    print("ツイートを取得します…")
    status_count = 0
    fav_count_list = []
    retweet_count_list = []
    datetime_list = []
    text_list = []
    for status in my_tweet:
        text = status.text
        # 投稿時間を取得して、日本時間に変換（９時間を足す）
        ja_datetime = status.created_at + datetime.timedelta(hours=9)
        # 1ヶ月ぶん取得したら終了
        if one_month_ago > ja_datetime:
            print("30日ぶんのツイートを取得しました")
            print("30日で{}件呟きました".format(status_count))
            break
        # メンションじゃなくて、1ヶ月前以降の投稿なら取得
        if "@" not in text and one_month_ago < ja_datetime < now:
            # ツイートの内容を取得してリストに追加
            text = status.text
            text_list.append(text)
            # いいね数を取得してリストに追加
            fav_count = status.favorite_count
            fav_count_list.append(fav_count)
            # リツイート数を取得してリストに追加
            retweet_count = status.retweet_count
            retweet_count_list.append(retweet_count)
            # 投稿時間をリストに追加
            datetime_list.append(ja_datetime)
            status_count += 1

    return (fav_count_list, retweet_count_list, datetime_list, text_list)
    

# 「いいね数・リツイート数・投稿時間」をデータフレームにして、順序を入れ替え
def convert_tweet_to_data_frame(my_tweet):
    # 「いいね数・リツイート数・投稿時間」を取得
    fav_count_list, retweet_count_list, datetime_list, text_list = get_my_tweet_one_month(my_tweet)
    # 各リストをデータフレームに変換
    df = pd.DataFrame([fav_count_list, retweet_count_list, datetime_list, text_list])
    df.index=["fav_count", "retweet_count", "datetime", "text_list"]
    # 欠格値を「0」で穴埋め
    df = df.fillna(0)
    # いいねが多い順にソート（ascending=Falseで降順（大きい順）になる）
    # 「axis=1」で行方向にソート、「inplace=True」で元のオブジェクトを上書き
    df.sort_values('fav_count', axis=1, ascending=False, inplace=True)
    # .Tプロパティの指定でindexとcolumnを入れ替える
    df = df.T
    
    return df
    
    
def Combine_it_at_the_same_time():
    df = convert_tweet_to_data_frame(my_tweet).head(30)
    # 「.drop」で要素を削除。「axis=0」なら行、1なら列
    df_drop = df.drop("text_list", axis=1)
    df.drop(df.index[df.fav_count == 0], axis=0, inplace=True)
    # 「.set_index()」で指定したcolumnがindexに変換
    df_i = df_drop.set_index('datetime')
    # 日付がindexの時に使える？
    # 「.resample()」で、引数に指定した内容（日付、月毎等）でまとめて「.sum()」でcolumnを合計
    df_t = df_i.resample("D").sum()
    # 縦のグラフ「kind='bar'」横のグラフ「kind='barh'」
    df_t.plot(kind='bar')
    plt.show()
    plt.savefig("{}/image.png".format(path))


if __name__ == "__main__":
    print(Combine_it_at_the_same_time())