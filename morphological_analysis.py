#!/usr/bin/env python
# coding:utf-8

# sudo find / -name dicrc　でpathを検索
# echo "○○" | mecab -d /usr/lib64/mecab/dic/mecab-ipadic-neologd/　で辞書を指定して形態素解析

import MeCab
import re
import types
import os
import pandas as pd
import csv
import get_my_timeline


# 自分のツイートを取得
my_tweet = get_my_timeline.my_tweet
path = os.path.dirname(os.path.abspath(__file__))


def word_tokenize(doc):
    print("形態素解析を行います…")
    '''形態素解析。パラメーターには
    「-d /usr/lib64/mecab/dic/mecab-ipadic-neologd/」を指定
    Swig Objectを作成
    '''
    tagger = MeCab.Tagger("-d /usr/lib64/mecab/dic/mecab-ipadic-neologd/")
    # parseToNode()を使う場合には一度.parse関数を呼び出さないとsurface属性が拾えない
    tagger.parseToNode("")
    word_list_all = []
    # 引数が短文か、listか確認。リストならループ
    if type(doc) is list:
        for v in doc:
            # Swig Objectをstr Objectに変換？
            result = tagger.parseToNode(v)
            word_list = []
            while result:
                # surfaceで単語、featureで解析結果を取得
                surface = result.surface
                # カンマ区切りの情報をカンマで分解し、最初の要素だけ拾う
                feature = result.feature.split(",")[0]
                analysis_list = (surface,feature)
                # 要素が「名詞」ならリストに追加
                if analysis_list[1] == "名詞":
                    word_list.append(analysis_list)
                # next属性を代入しないと無限ループ？
                result = result.next
            word_list_all.extend(word_list)
        return word_list_all
    else:
        # Swig Objectをstr Objectに変換？
        result = tagger.parseToNode(doc)
        word_list = []
        while result:
            # surfaceで単語、featureで解析結果を取得
            surface = result.surface
            # カンマ区切りの情報をカンマで分解し、最初の要素だけ拾う
            feature = result.feature.split(",")[0]
            analysis_list = (surface,feature)
            # 要素が「名詞」ならリストに追加
            if analysis_list[1] == "名詞":
                word_list.append(analysis_list)
            # next属性を代入しないと無限ループ？
            result = result.next
        word_list_all.extend(word_list)
    return word_list_all


def word_count_method(doc):
    word_list_all = word_tokenize(doc)
    # {品詞：回数}を入れる想定で辞書を作成
    word_cound_dic = {}
    for w in word_list_all:
        part = w[0]
        # 初登場の場合は辞書のkeyに追加。2回目以降は回数を加算
        if part not in word_cound_dic:
            word_cound_dic[part] = 1
        else:
            word_cound_dic[part] += 1
    
    after_sorted_key = []
    after_sorted_values = []
    # valueを降順でソート
    for k, v in sorted(word_cound_dic.items(), key=lambda x: -x[1]):
        after_sorted_key.append(k)
        after_sorted_values.append(v)
        
    # リストをcsv化
    df = \
    pd.DataFrame([after_sorted_key, after_sorted_values]).T
    df.columns=["word", "count"]
    
    path = os.path.dirname(os.path.abspath(__file__))
    df.to_csv("{}/morphological_analysis.csv".format(path))
    print("解析結果をcsvに書き込みました！")
    
    return after_sorted_key


if __name__ == "__main__":
    # 「.text_list」でdfからcolumnを取り出して、「.values.tolist()」でリストに変換
    text_list = get_my_timeline.convert_tweet_to_data_frame(my_tweet).text_list.values.tolist()
    # 名詞のリストを作成
    list_of_nouns = word_count_method(text_list)
    # リストを文字列に変換
    text = ",".join(list_of_nouns)
