import requests
import lxml.html
import json
import os

# Magic constant
QUERY_HASH = '003056d32c2554def87228bc3fd9668a'
# Max post count for 1 request
POST_COUNT = 50

# Protect from redirect
HEADERS = {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}


def _get_user_nick():
    """
    Read nick from nick.txt
    :return nick(str): user nick
    """
    return open('nick.txt').read()


def _get_html_page():
    """
    Get html page for parse
    :return html_page(html): page from instagram.com/nick/
    """
    response = requests.get(f'https://www.instagram.com/{USER_NICK}', headers=HEADERS)
    if response.url != 'https://www.instagram.com/account/login/':
        html_page = response.text
        return html_page
    else:
        print("Too much requests. Try again later.")
        exit()


def _get_script(html_page):
    """
    Search script for get first 12 posts
    :param html_page(html): page from instagram.com/nick/
    :return script(json): json info about 12 posts
    """
    tree = lxml.html.fromstring(html_page)
    script = json.loads(tree.xpath('/html/body/script[1]/text()')[0][len('window._sharedData = '):-1:])
    return script


def _get_user_id(script: json):
    """
    :param script(json): info about 12 posts
    :return id: user id
    """
    return script['entry_data']['ProfilePage'][0]['graphql']['user']['id']


def _get_after(script: json):
    """
    :param script(json): info about next page
    :return after: pointer to next request
    """
    page_info = script['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']
    if page_info['has_next_page']:
        return page_info['end_cursor']
    else:
        return None


def _save_firs_posts(script):
    """
    :param script: info about first 12 posts
    :return: save posts
    """
    user = script['entry_data']['ProfilePage'][0]['graphql']['user']
    edges = user['edge_owner_to_timeline_media']['edges']
    for edge in edges:
        node = edge['node']
        save_posts(node)


def save_posts(node):
    """
    :param node(json):info about
    :return: save posts
    """
    try:
        children = node['edge_sidecar_to_children']
        edges = children['edges']
        for edge in edges:
            node = edge['node']
            is_video = node['is_video']
            if not is_video:
                url = node['display_url']
                save_pic(url)
            else:
                url = node['video_url']
                save_video(url)
    except:
        is_video = node['is_video']
        if not is_video:
            url = node['display_url']
            save_pic(url)
        else:
            url = node['video_url']
            save_video(url)


def save_pic(url):
    """
    :param url: url for pic
    :return: save pic by url
    """
    if not os.path.exists(USER_NICK):
        os.mkdir(USER_NICK)
    count = len(os.listdir(USER_NICK))
    with requests.get(url, stream=True) as response:
        name = count + 1
        with open(f'{USER_NICK}/{name}.jpg', 'wb') as pic:
            for chunk in response.iter_content(chunk_size=4096):
                pic.write(chunk)
    return name


def save_video(url):
    """
    :param url: url for video
    :return: save pic by video
    """
    if not os.path.exists(USER_NICK):
        os.mkdir(USER_NICK)
    count = len(os.listdir(USER_NICK))
    with requests.get(url, stream=True) as response:
        name = count + 1
        with open(f'{USER_NICK}/{name}.mp4', 'wb') as pic:
            for chunk in response.iter_content(chunk_size=4096):
                pic.write(chunk)
    return name


USER_NICK = _get_user_nick()
_HTML_PAGE = _get_html_page()
_SCRIPT = _get_script(_HTML_PAGE)
USER_ID = _get_user_id(_SCRIPT)
AFTER = _get_after(_SCRIPT)
_save_firs_posts(_SCRIPT)
