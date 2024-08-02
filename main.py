import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Union
from os.path import basename

ANIME_FIRE_URL = "https://animefire.plus/"
def make_html(html):
    with open("animefire.html", "w") as f:
        f.write(html)

def make_json(obj):
    with open("anime_ep_json.json", 'w') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)

def get_anime_eps(soup:BeautifulSoup):
    url_list = []
    soup_eps = soup.find_all('div', attrs={'class':'divCardUltimosEpsHome'})

    for ep in soup_eps:
        ep_url = ep.find('a')
        url_list.append(ep_url)
    
    return url_list

def get_url_links(url_list:list[str]):
    urls_content = []
    for url in url_list:
        url = url['href']
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        urls_content.append(soup)
        # print(soup.title.text)
        # <title></title>
        
    return urls_content

def get_json_file_video(json_url):
    obj_video = requests.get(json_url).text
    string_obj = json.loads(obj_video)  # json -> obj python
    print(string_obj)
    # make_json(string_obj)
    # json.dump()  # obj python -> json
    # print(obj_video)

    list_ep = string_obj.get('data')
    ep = list_ep[-1]
    ep = ep.get('src')
    # print(f'episodio: {ep}')
    return ep

def get_informations_ep(ep_page:BeautifulSoup):
    div_info = ep_page.find('div', attrs={'class':'divInformacoes'})
    date = div_info.find('h6').text.replace('Publicado Dia:','').strip()
    print(date)
    sinopse = div_info.find('p', attrs={'id':'video_sinopse'}).text.strip().replace('Sinopse:','').strip()
    print(sinopse)

    return date, sinopse

def get_ep_video(urls_content:list[BeautifulSoup]):
    
    anime_ep_list = []

    for ep_page in urls_content:
        # make_html(ep_page.prettify())
        video = ep_page.find('video', attrs={'id':'my-video'})
        video_json = video['data-video-src']
        video = get_json_file_video(video_json)
        date, sinopse = get_informations_ep(ep_page)
        
        obj = {
            'video':video,
            'date':date,
            'sinopse':sinopse
        }
        anime_ep_list.append(obj)

    return anime_ep_list

def download_goku_flamenguista():
    url_video='https://media.istockphoto.com/id/1534881240/pt/v%C3%ADdeo/serious-small-business-owner-with-arms-crossed-standing-inside-grocery-store-chain-concerned.mp4?s=mp4-640x640-is&k=20&c=dFEJeVFX-3-AiE3TtcXRrTt7o_gRQavBGO6_Z8ID-sA='
    url_image='https://i.pinimg.com/474x/98/50/78/9850789a6980c816682831c89931cc3c.jpg'
    image_bin = requests.get(url_image).content
    image_name = 'Goku Flamenguista.' + basename(url_image).split('.')[1]
    video_bin = requests.get(url_video).content
    video_name = 'vei.mp4'

    with open(image_name, 'wb') as f:
        f.write(image_bin)
        f.close()
    
    with open(video_name, 'wb') as f:
        f.write(video_bin)
        f.close()

# content =  requests.get(ANIME_FIRE_URL).content
# soup = BeautifulSoup(content, "html.parser")
# make_html(soup.prettify())
# url_list_ep = get_anime_eps(soup)
# urls_content = get_url_links(url_list_ep)
# anime_ep_list = get_ep_video(urls_content)
# make_json({'animes':anime_ep_list})
download_goku_flamenguista()
# print(soup.prettify())