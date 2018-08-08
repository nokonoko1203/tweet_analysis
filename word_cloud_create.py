#!/usr/bin/env python
# coding:utf-8


import os
import get_my_timeline
import morphological_analysis
from wordcloud import WordCloud
import matplotlib
# cloud9では以下を指定しないとエラーがでる
matplotlib.use('Agg')
# 上記記述後に「.pyplot」をimportすること
import matplotlib.pyplot as plt


# 自分のツイートを取得
my_tweet = get_my_timeline.my_tweet
path = os.path.dirname(os.path.abspath(__file__))


def print_word_cloud(text):
    print("ツイートを可視化しています…")
    # 日本語を利用するなら「fpath」が必要。「wordcloud」の引数にも追加すること
    """
    centOSの場合は日本語フォントが入っていない？
    →「sudo yum install ipa-gothic-fonts ipa-pgothic-fonts」でインストール
    →「rpm -ql ipa-gothic-fonts.noarch」でyumでインストールしたもののパスを確認
    →拡張子が「.ttf」の物を「fpath」に指定
    """
    fpath = "/usr/share/fonts/ipa-gothic/ipag.ttf"
    
    # あまり意味のなさそうな言葉をストップワードとして設定
    stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
             u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
             u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
             u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

    wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500, stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15,12))
    # 「.imshow」で「wordcloud」を貼りつけ
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file("{}/word_cloud.png".format(path))
    print("完了しました！")
    

if __name__ == "__main__":
    # 「.text_list」でdfからcolumnを取り出して、「.values.tolist()」でリストに変換
    text_list = get_my_timeline.convert_tweet_to_data_frame(my_tweet).text_list.values.tolist()
    # 名詞のリストを作成
    list_of_nouns = morphological_analysis.word_count_method(text_list)
    # リストを文字列に変換
    text = ",".join(list_of_nouns)
    # テキストの可視化
    print_word_cloud(text)