import requests
import settings


def main():
    URL = 'https://www.instagram.com/graphql/query'
    with requests.session() as s:
        while True:
            variables = f"""{{
                "id": \"{settings.USER_ID}\",
                "first": \"{settings.POST_COUNT}\",
                "after": \"{settings.AFTER}\"
                }}"""
            params = {"query_hash": settings.QUERY_HASH,"variables": variables}
            response = s.get(URL, headers=settings.HEADERS, params=params)
            if response.status_code == 200:
                response = response.json()
                edges = response['data']['user']['edge_owner_to_timeline_media']['edges']
                for edge in edges:
                    node = edge['node']
                    settings.save_posts(node)
                page_info = response['data']['user']['edge_owner_to_timeline_media']['page_info']
                if page_info['has_next_page']:
                    settings.AFTER = page_info['end_cursor']
                else:
                    break
            else:
                print(response.status_code)
                break


if __name__ == '__main__':
    main()
