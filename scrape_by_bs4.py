#!/usr/bin/python3

from bs4 import BeautifulSoup

# HTMLファイルを読み込んでBeautifulSoupオブジェクトを得る。
with open('./aiit.ac.jp/master_program/isa/index.html') as f:
    soup = BeautifulSoup(f, 'html.parser')
f.close

# find_all()メソッドでa要素のリストを取得して、個々のa要素に対して処理を行う。
for a in soup.find_all('a'):
    print(a.get('href'), a.text)  # href属性とリンクのテキストを取得して表示する。

