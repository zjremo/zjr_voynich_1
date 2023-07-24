import requests
from bs4 import BeautifulSoup
import random

import re
import csv

# 随机给出请求头中的 user-agent
# 模拟多个 user-agent，随机选取 list 中的一个
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
# 完成随机选取 user-agent，实现 反 反爬 操作
request_headers = {
    'user-agent': random.choice(user_agents),
    "Connection": "keep-alive",
    "Referer": "https://tj.zu.anjuke.com"
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
            # 调用方法，获取每一一个评价页面中的信息
            link = a_element.get('link')
            scrape(link)


def scrape(url):
    response = requests.get(url, headers=request_headers)
    status_cod = response.status_code
    if status_cod == 200:
        html = response.text

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 查找指定的 div 标签
        div = soup.select_one('body > div.wrapper > div.mainbox.cf > div.lbox > div:nth-child(2) > div ')
        div2 = soup.select_one("div.lbox > ul.house-info-zufang.cf ")

        if div:
            id = div.text.strip()  # 获取 <div class="right-info"> 元素的文本内容，并去除首尾空格
        if div2:
            info = div2.text.strip() + id
            # 处理字符串，转化为列表方便输出
            result = extract_info_from_string(info)
            with open(file_path, 'a', encoding='UTF-8', errors='ignore', newline="") as csvf:
                writer1 = csv.writer(csvf)
                # 将列表写入CSV文件的一行
                writer1.writerow(result)
                print(result)


def extract_info_from_string(text):
    rent_match = re.search(r'(\d+)元/月', text)
    rent = rent_match.group(1) if rent_match else " "

    layout_match = re.search(r'户型：\n(.+)', text)
    layout = layout_match.group(1) if layout_match else " "

    area_match = re.search(r'面积：\n(.+)', text)
    area = area_match.group(1) if area_match else " "

    orientation_match = re.search(r'朝向：\n(.+)', text)
    orie = orientation_match.group(1) if orientation_match else " "

    floor_match = re.search(r'楼层：\n(.+)', text)
    floor = floor_match.group(1) if floor_match else " "

    decoration_match = re.search(r'装修：\n(.+)', text)
    deco = decoration_match.group(1) if decoration_match else " "

    house_type_match = re.search(r'类型：\n(.+)', text)
    house_type = house_type_match.group(1) if house_type_match else " "

    community_match = re.search(r'小区：\n(.+)', text)
    community = community_match.group(1) if community_match else " "

    matches = re.findall(r"\((.*?)\)", text)
    if len(matches) >= 2:
        street = matches[1]
    else:
        street = " "

    house_code_match = re.search(r'房屋编码：(\d+)', text)
    house_code = house_code_match.group(1) if house_code_match else " "

    update_time_match = re.search(r'更新时间：(\d+年\d+月\d+日)', text)
    update = update_time_match.group(1) if update_time_match else " "

    lines = text.splitlines()  # 按行拆分字符串
    payment = lines[1]
    # 将提取的信息存储在列表中
    info_list = [rent, payment, layout, area, orie, floor, deco, house_type, community, street, house_code, update]
    return info_list


def extract_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # 读取并保存标题行

        # 创建一个字典，用于存储相同第11列值的行
        merged_rows = {}

        # 迭代读取 CSV 文件中的每一行
        for row in csv_reader:
            key = row[10]  # 第11列的索引为10，根据实际情况调整
            if key in merged_rows:
                merged_rows[key].extend(row)  # 将当前行内容添加到已存在的行中
            else:
                merged_rows[key] = row  # 创建新的行

    # 将合并后的行写入新的 CSV 文件
    with open(path, 'w', newline='', encoding='UTF-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)  # 写入标题行
        for key, values in merged_rows.items():
            csv_writer.writerow(values)


# 声明主程序入口
if __name__ == '__main__':
    file_path = "E:\\python\\pycharm\\projects\\pythonProject1\\house\\house_info.csv"
    # for i in range(1, 51):
    #     print(i)
    #     url = f"https://tj.lianjia.com/zufang/p{i}"
    #     get_per_divs(url)
    extract_file(file_path)
    print("End....")
