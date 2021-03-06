import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import feedgenerator


def main():
    """
    メインの処理。
    """

    driver = webdriver.PhantomJS()  # PhantomJSのWebDriverオブジェクトを作成する。
    driver.set_window_size(800, 600)  # ウィンドウサイズを設定する。

    navigate(driver)  # noteのトップページに遷移する。
    posts = scrape_posts(driver)  # 文章コンテンツのリストを取得する。

    # RSSフィードとして保存する。
    with open('recommend.rss', 'w') as f:
        save_as_feed(f, posts)


def navigate(driver):
    """
    目的のページに遷移して続きのコンテンツを読み込む。
    """

    print('Navigating...', file=sys.stderr)
    driver.get('https://note.mu/')  # noteのトップページを開く。
    assert 'note' in driver.title  # タイトルに'note'が含まれていることを確認する。
    time.sleep(2)  # 2秒間待つ。

    # ページの一番下までスクロールする。
    driver.execute_script('scroll(0, document.body.scrollHeight)')

    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)  # 2秒間待つ。

    # ページの一番下までスクロールする。
    driver.execute_script('scroll(0, document.body.scrollHeight)')

    # 10秒でタイムアウトするWebDriverWaitオブジェクトを作成する。
    wait = WebDriverWait(driver, 10)

    print('Waiting for the more button to be clickable...', file=sys.stderr)
    # 「もっとみる」ボタンがクリック可能になるまで待つ。
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-more')))

    button.click()  # 「もっとみる」ボタンをクリックする。

    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)  # 2秒間待つ。


def scrape_posts(driver):
    """
    文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する。
    """

    posts = []

    # すべての文章コンテンツを表す<a>要素について反復する。
    for a in driver.find_elements_by_css_selector('a.p-post--basic'):
        # URL、タイトル、概要を取得して、dictとしてリストに追加する。
        posts.append({
            'url': a.get_attribute('href'),
            'title': a.find_element_by_css_selector('h4').text,
            'description': a.find_element_by_css_selector('.c-post__description').text,
        })

    return posts


def save_as_feed(f, posts):
    """
    文章コンテンツのリストをフィードとして保存する。
    """

    # フィードを表すRss201rev2Feedオブジェクトを作成する。
    feed = feedgenerator.Rss201rev2Feed(
        title='おすすめノート',  # フィードのタイトル
        link='https://note.mu/',  # フィードに対応するWebサイトのURL
        description='おすすめノート')  # フィードの概要

    for post in posts:
        # フィードにアイテムを追加する。
        # キーワード引数unique_idは、アイテムを一意に識別するユニークなIDを指定する。
        # 必須ではないが、このIDを指定しておくとRSSリーダーがアイテムの重複なく扱える
        # 可能性が高まるので、ここではコンテンツのURLを指定している。
        feed.add_item(title=post['title'], link=post['url'],
                      description=post['description'], unique_id=post['url'])

    feed.write(f, 'utf-8')  # ファイルオブジェクトに書き込む。第2引数にエンコーディングを指定する。

if __name__ == '__main__':
    main()
