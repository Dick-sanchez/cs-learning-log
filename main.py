print('run')
from bs4 import BeautifulSoup
import requests
import time
import csv
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

all_movies = [] #初始化列表

for page in range(10):
    url = f'https://movie.douban.com/top250?start={page * 25}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find_all('div', class_='item')
    for movie in movies:
        info = movie.find('div', class_='info')
        title = info.find('div', class_='hd').find('a').find('span').text
        rating = info.find('div', class_='bd').find('div').find('span', class_='rating_num').text
        tag = info.find('div', class_='bd').find('p').text.strip()
        parts = movie.find('div', class_='bd').find('p').get_text(separator='|').split('|')
        year = parts[1].strip() if len(parts) > 1 else ''

        # 再从year里分出 年份、国家、类型（用/分隔）

        year_info = year.split('/')
        year_val = year_info[0].strip()
        country = year_info[1].strip() if len(year_info) > 1 else ''
        genre = year_info[2].strip() if len(year_info) > 2 else ''
        all_movies.append([title, rating, year_val, country, genre])

        
with open('douban_top250.csv', 'w', newline='', encoding='gbk') as f:
    writer = csv.writer(f)
    writer.writerow(['电影名', '评分', '年份', '国家', '类型'])
    for movie in all_movies:
        writer.writerow(movie)

print('success')
        
    
