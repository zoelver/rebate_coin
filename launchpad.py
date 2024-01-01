#!/usr/bin/env python
# -*- coding:utf-8 -*-

from time import sleep
from playwright.sync_api import sync_playwright
from config import tracking_path
import os
import json


file_is_exists = os.path.join(tracking_path(), '.')




def mk_dir(path):
    ''' 创建目录 '''
    # 引入模块
    # import os

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path+' 目录已存在')
        return False
def file_python_exists(file_path):
    return os.path.exists(file_path)
def remove_folder(folder_path):
    ''' 
    会直接删除整个文件夹及其内容.在使用方法2时,需要确保路径有效性,以免意外删除其他文件夹 
    '''
    # 指定要删除的文件夹路径
    # folder_path = "your/folder/path"
    if not file_python_exists(folder_path) :
        return ''
    
    # 获取文件夹内所有文件名
    file_names = os.listdir(folder_path)
    
    # 遍历并删除每个文件
    for file in file_names:
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path)  or os.path.islink(file_path):
            # 如果是文件则直接删除
            os.remove(file_path)
            
        elif os.path.isdir(file_path):
            # 如果是子文件夹则递归调用该函数进行删除操作
            remove_folder(file_path)
            os.rmdir(file_path)
    # os.rmdir(folder_path)

def append_to_jsonl(file_path, data):
    # 将数据转换为JSON格式  
    json_data = json.dumps(data,ensure_ascii=False)
  
    # 追加写入到.jsonl文件中  
    with open(file_path, 'a',encoding='utf-8') as file:  
        file.write(json_data + '\n')  

# 创建目录
mk_dir(file_is_exists)

def print_request_sent(request):
    url = request.url
    if url.__contains__('/listV3'):
        print("Request sent: " + request.url)

def print_request_finished(request):
    url = request.url
    if url.__contains__('/listV3'):
        hds = request.all_headers()
        # print("Request finished: " + url)
        print('')
        # print("Request hds: " ,hds)
        print('')
        rest = request.response()
        # print("Request rest: " ,rest.text()  )
        # print('')
        json_data = rest.json() 
        # print("Request json: " , json_data['data']['tracking'][0]['rebateCoin'],type(json_data) )
        is_new_coin_list = []
        for item in json_data['data']['tracking']:
            rebateCoin = item['rebateCoin']
            # print('--rebateCoin--', rebateCoin)
            file_rebate_coin = os.path.join(tracking_path(), '{}.json'.format(rebateCoin) )
            if not file_python_exists(file_rebate_coin) :
                append_to_jsonl(file_rebate_coin, rebateCoin)
                is_new_coin_list.append(rebateCoin)
        print('')
        if is_new_coin_list:
            print('--is_new_coin_list--', is_new_coin_list)



def get_context_page(playwright):
    chromium = playwright.chromium
    # headless=True 无界面模式
    # slow_mo 暂停多少毫秒
    browser = chromium.launch(headless=True,slow_mo=100)
    # viewport 浏览器界面的大小
    browser_context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    # browser_context.add_init_script(path="stealth.min.js")
    context_page = browser_context.new_page()
    return browser_context,context_page


def run():

    url = os.environ.get("OPEN_URL") or ''
    if url:
        playwright = sync_playwright().start()
        browser_context, context_page = get_context_page(playwright)

        # context_page.on("request", print_request_sent)
        context_page.on("requestfinished", print_request_finished)

        context_page.goto(url)
        # 暂停
        context_page.wait_for_timeout(2000)

        sleep(5)
        context_page.close()
        browser_context.close()
        playwright.stop()


if __name__ == "__main__":
    cookieStr = '''https://launchpad.binance.com/zh-CN'''
    os.environ.setdefault("OPEN_URL", cookieStr)
    run()















# launchpad.py







