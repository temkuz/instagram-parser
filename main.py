import requests
import settings
import os


def first_download():
    settings._HTML_PAGE = settings._get_html_page()
    settings._SCRIPT = settings._get_script(settings._HTML_PAGE)
    settings.USER_ID = settings._get_user_id(settings._SCRIPT)
    settings.AFTER = settings._get_after(settings._SCRIPT)
    settings._save_firs_posts(settings._SCRIPT)


def main():
    URL = 'https://www.instagram.com/graphql/query'
    i = 1
    with requests.session() as s:
        while True:
            variables = f"""{{
                "id": \"{settings.USER_ID}\",
                "first": \"{settings.POST_COUNT}\",
                "after": \"{settings.AFTER}\"
                }}"""
            params = {"query_hash": settings.QUERY_HASH, "variables": variables}
            response = s.get(URL, headers=settings.HEADERS, params=params)
            if response.status_code == 200:
                response = response.json()
                edges = response['data']['user']['edge_owner_to_timeline_media']['edges']
                for edge in edges:
                    node = edge['node']
                    settings.save_posts(node)
                    os.system('cls')
                    print('Poccess', end='')
                    print('.' * (i % 4))
                    i += 1
                page_info = response['data']['user']['edge_owner_to_timeline_media']['page_info']
                if page_info['has_next_page']:
                    settings.AFTER = page_info['end_cursor']
                else:
                    os.system('cls')
                    print('Finish')
                    break
            else:
                print('Wrong status code')
                break


if __name__ == '__main__':
    first_download()
    main()
