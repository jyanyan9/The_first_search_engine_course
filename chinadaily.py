# -*- coding: UTF-8 -*-
import datetime
import requests
import sys

def get_new(start_day, end_day):
    url = f'http://newssearch.chinadaily.com.cn/rest/cn/search?publishedDateFrom={start_day}&publishedDateTo={end_day}&channel=&type=&curType=story&duplication=on&page=0&type%5B0%5D=story&type%5B1%5D=comment&type%5B2%5D=blog&type%5B3%5D=photo&channel%5B0%5D=2%40webnews&channel%5B1%5D=2%40bw&channel%5B2%5D=ismp%40cndyglobal&source='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.9 Safari/537.36'
    }
    rep = requests.get(url, headers=headers)
    page_num = rep.json()['totalPages']
    for _ in range(int(page_num)):
        page = f'page={_}'
        url_ = url.replace('page=0', page)
        rep_ = requests.get(url_, headers=headers)
        contents = rep_.json()['content']
        for content in contents:
            Text = content['plainText']
            if Text is None:
                pass
            else:
                global num
                num += 1
                print("Done:",num)
                vase_info(num, Text)


def vase_info(num, Text):
    global new_num
    new_num = new_num + 1
    if sys.getsizeof(Text) >= 20*1024:
        with open(f'./数据/{num}.txt', 'w', encoding='utf-8') as f:
            f.write(Text)
            print(new_num, '符合要求')
            print('-' * 100)




if __name__ == '__main__':
    num = 0
    new_num = 0
    start_day = input('请输入开始日期:')
    end_day = input('请输入结束日期:')
    start_day = str(datetime.datetime.strptime(start_day, "%Y%m%d")).split(' ')[0]
    end_day = str(datetime.datetime.strptime(end_day, "%Y%m%d")).split(' ')[0]
    get_new(start_day, end_day)  # 2023-04-05
