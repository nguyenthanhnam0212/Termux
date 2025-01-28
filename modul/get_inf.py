from bs4 import BeautifulSoup
import requests
import re

def get_uralesbian(page):
    url = f"https://www.sakurajav.com/ura-lesbian/page/{page}"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    zone = soup.find("div", class_="videos-list-isCategory")
    links = zone.find_all("a")
    arr_links = [i.get("href") for i in links]
    return arr_links

def get_uralesbian_poster(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    zone = soup.find("div", class_="video-player")
    script_tag = zone.find('script')
    match = re.search(r'poster:\s*"([^"]+)"', script_tag.string)
    if match:
        poster_url = match.group(1).replace("\\/", "/")  # Sửa dấu gạch chéo
    return poster_url

def process_link(link_poster):
    arr = link_poster.split("/")
    arr_actor = arr[4].split("_")[:-1]
    caption = f"#UraLesbian {arr_actor[0]}\n"
    arr_actor = arr[4].split("_")[:-1][1:]
    for i in arr_actor:
        caption = caption + f"#{i}   "
    return caption.strip()