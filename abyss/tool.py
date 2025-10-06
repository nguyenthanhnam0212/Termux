from bs4 import BeautifulSoup
import requests
import asyncio
import re
import urllib.parse

class CRAW():
    def add_row(page):

        url = f'https://tvhayd.org/phim-le/?sort=default&page={page}'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        zone = soup.find('ul', class_='list-film')
        List_Zone = zone.find_all('div', class_='inner')
        name = []
        for i in List_Zone:
            a_tag = i.find('a')
            name_vn = a_tag.get('title')
            link = a_tag.get('href')
            name_en = i.find('div', class_='name2').text.strip()
            name.append(name_vn)
        return name

    def get_url(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        zone = soup.find('a', class_='btn-watch')
        link_detail = f"https://chillhayk.pro{zone.get("href")}"
        response = requests.get(link_detail)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # zone_info = soup.find('div', class_='dinfo fr')
        # l = zone_info.find_all('dd')
        # url2 = zone.find('a').get('href')
        # response = requests.get(url2)
        # soup2 = BeautifulSoup(response.text, 'html.parser')
        # zone2 = soup2.find('ul', class_='episodelistsv')
        # try:
        #     link = zone2.find('a', text = 'H.PRO').get('href')
        # except:
        #     link = ""
        # return link

X = CRAW.add_row(142)
print(X)






