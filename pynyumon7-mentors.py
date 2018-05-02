#!/usr/bin/python3
#
import requests
from bs4 import BeautifulSoup

def main():

    # connpass の PyNumon#7 のイベント参加者・申込者一覧のURL
    url = 'https://python-nyumon.connpass.com/event/83667/participation'

    # requests で参加者一覧の情報と取得する
    response = requests.get(url)

    # response に対して、文字化け防止のおまじない(念のため追加)
    response.encoding = 'utf-8'

    # response から HTML 部分(content) を取得
    content = response.content

    # BeautifulSoup に content を渡して解析の準備をする
    soup = BeautifulSoup(content, 'html.parser')

    # <div class="participation_table_area mb_20">  に該当するものを取り出す
    # participation_tables は List
    #participation_tables = soup.find_all('table', class_='common_table participants_table padding_10')
    participation_tables = soup.find_all('div', class_='participation_table_area mb_20')

    # participation_tables を順番に見て、"講師・メンター枠"の情報を取り出す
    mentors_table = []
    for participation_table in participation_tables:
        # <thead><tr><th> に該当するタグの要素を取り出す (参加者枠の種類が記載されているので)
        #participant_type = participation_table.table.thead.tr.th.get_text()
        participant_type = participation_table.thead.tr.th.get_text(strip=True)

        # 参加者枠を示す文字に "講師・メンター枠" が含まれるものを取り出す
        if '講師・メンター枠' in participant_type:
            mentors_table = participation_table
            break

    # 講師・メンター枠の HTML の中で class=user_info に該当するものをまとめて一式取り出す
    # mentor_infos は List
    #mentor_infos = mentors_table.find_all(class_=['display_name','user_profile'])
    mentor_infos = mentors_table.find_all(class_='user_info')
    # ついでに、講師・メンターの人数も取り出す
    mentor_count = mentors_table.find(class_='participants_count')

    # 取り出した 講師・メンター枠の要素から名前(前後の無駄な空行や改行などを取り除く)とプロフィールを連結して表示
    for mentor_info in mentor_infos:
        #print(mentor_info.get_text().strip())
        display_name = mentor_info.find(class_='display_name').get_text().strip()
        user_profile = mentor_info.find(class_='user_profile').get_text()
        print(display_name + ' | ' + user_profile)

    print('------------')
    # 最後に講師・メンターの人数も表示
    print(mentor_count.get_text())


if __name__ == '__main__':
    main()
