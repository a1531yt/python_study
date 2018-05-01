#!/usr/bin/python3
#
from feedparser import parse

# AIITイベントの RSSを読み込む。
d = parse('https://aiit.ac.jp/events.rss')


# すべての要素について処理を繰り返す。
for entry in d.entries:
    print(entry.link, entry.title)

