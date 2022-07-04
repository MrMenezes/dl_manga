
import requests
from bs4 import BeautifulSoup
import re
from load import print_progress

site = 'https://muitomanga.com/manga/adonis-next-door'

def list_chapters(site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')

    name = soup.find('h1', class_='subtitles_menus').text
    name_url = re.compile(r'/+[\w-]*\b').findall(site)[-1]
    manga = { 'chapters': [], 'name': name, 'name_url': name_url }
    chapters = soup.find_all('div', class_='single-chapter')

    for chapter in chapters:
        chapter_link = chapter.find('a')['href']
        chapter_name = chapter.find('a').text
        # print(f'{chapter_name} - {prefix + chapter_link}')
        manga['chapters'].append({ 'name': chapter_name, 'link': chapter_link})

    return manga

def pages_chapter(chapter, name, name_url, download_path=None):
    chapter_number = re.compile(r'\d+').findall(chapter['link'])[0]
    chapter['number'] = chapter_number
    chapter['pages'] = []
    page = 2
    while True:
        url = f'https://cdn.statically.io/img/imgs.muitomanga.com/f=auto/imgs/{name_url}/{chapter_number}/{page}.jpg'
        page_req = requests.get(url) if download_path else requests.head(url)
        if page_req.status_code != 200:
            break
        chapter['pages'].append({'link': url})
        if download_path:
            import os
            os.makedirs(download_path, exist_ok=True)
            with open(f"{download_path}/{name} - {chapter['name']} - {page-1}.jpg", 'wb') as f:
                f.write(page_req.content)
        # print(f'{name} - {chapter['name']} - {page}.jpg')
        page += 1

def load_chapters(manga, download_path=None):
    percent = 0
    total = 0
    for chapter in manga['chapters']:
        pages_chapter(chapter, manga["name"], manga["name_url"],download_path)
        if total == 0:
            total = int(chapter['number'])
        percent = (total - int(chapter['number']) + 1 ) / total * 100
        print_progress(percent)


# manga = list_chapters(site)
# load_chapters(manga)
manga = {'name': 'Adonis Next Door'}
from zip import zip
zip(f'downloads/{manga["name"]}', manga["name"])
