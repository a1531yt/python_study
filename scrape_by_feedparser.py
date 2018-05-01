#!/usr/bin/python3
#
from feedparser import parse

# はてなブックマークの人気エントリー（「テクノロジー」カテゴリ）のRSSを読み込む。
d = feedparser.parse('http://d.hatena.ne.jp/pklib/rss')

# すべての要素について処理を繰り返す。
for entry in d.entries:
    print(entry.link, entry.title)

