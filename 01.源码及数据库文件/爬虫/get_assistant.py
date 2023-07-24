import requests
from bs4 import BeautifulSoup
import random
import re
import csv
import time

# 随机给出请求头中的 user-agent
edge_us = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
]

request_headers = {
    'user-agent': random.choice(edge_us),
    "Connection": "keep-alive",
    "Referer": "https://tj.zu.anjuke.com/fangyuan/"
}


def get_per_divs(url):
    web_data = requests.get(url=url, headers=request_headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        # 解析为 soup 文档
        soup_document = BeautifulSoup(html_text, 'html.parser')
        # 定位到所有评价href标签
        a_elements = soup_document.find_all('div', class_='zu-itemmod')
        # 遍历每一个href
        for a_element in a_elements:
            # 调用方法，获取每一个详情页面中的信息
            link = a_element.get('link')
            get_assi(link)


def get_assi(url):
    response = requests.get(url, headers=request_headers)
    status_cod = response.status_code
    if status_cod == 200:
        html = response.text

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 查找指定的 div 标签
        qa_div = soup.select_one('div.lbox > div.comm-jiedu > ul > li > div.comment-info')
        name_div = soup.select_one('#commArround')
        if qa_div:
            name = name_div.text.strip()
            qa = qa_div.text.strip()  # 获取 <div class="right-info"> 元素的文本内容，并去除首尾空格

            # 处理字符串，转化为列表方便输出
            result = extract_info_from_string(name, qa)
            with open(file_path, 'a', encoding='UTF-8', errors='ignore', newline="") as csvf:
                writer1 = csv.writer(csvf)
                # 将列表写入CSV文件的一行
                for qa in result:
                    writer1.writerow(qa)
                    print(qa)
                    time.sleep(0.2)


def extract_info_from_string(name, text):
    pattern = r'【(.*?)】(.*?)\n'
    matches = re.findall(pattern, text)
    information = []
    for match in matches:
        category = match[0]
        content = match[1]
        information.append([name, category, content])
    # 添加"不足之处"的信息
    if "不足\n" in text:
        drawbacks = text.split("不足\n")[1].strip()
        information.append([name, "不足之处", drawbacks])
    return information


def extract_csv(file_path, out_path):
    # 打开CSV文件
    with open(file_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # 创建一个字典，用于存储相同前两个元素的行
    merged_rows = {}

    # 遍历每一行数据
    for row in rows:
        key = (row[0], row[1])  # 使用前两个元素作为键
        if key in merged_rows:
            merged_rows[key].extend(row[2:])  # 将第三个元素及之后的元素添加到已存在的行中
        else:
            merged_rows[key] = row[2:]  # 创建新的行

    # 将合并后的行写入新的CSV文件
    with open(out_path, 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        for key, values in merged_rows.items():
            writer.writerow(key + tuple(values))


# 声明主程序入口
if __name__ == '__main__':
    file_path = "E:\\python\\pycharm\\projects\\pythonProject1\\house\\assistant_info.csv"
    out_path = "E:\\python\\pycharm\\projects\\pythonProject1\\house\\assistant_info_out.csv"
    for i in (1, 51):
        print(i)
        url = f"https://tj.zu.anjuke.com/fangyuan/p{i}"
        get_per_divs(url)
    extract_csv(file_path, out_path)
    print("End....")
