from __future__ import print_function

import json
import sys

import html_to_json
import requests
from bs4 import BeautifulSoup

from oauth2client import client
from googleapiclient import sample_tools

SCOPE = 'https://www.googleapis.com/auth/blogger'


def poster(robotable_url: str, title: str, posts):
    try:
        with open('settings.json', encoding='utf-8') as f:
            settings = json.load(f)
            blog_id = str(settings['blogID'])
            post_id = str(settings['postID'])

        body = posts.get(blogId=blog_id, postId=post_id).execute()
        body['content'] = body[
                              'content'] + '<a href="' + robotable_url + '">' + robotable_url + '</a> ' + title + '<br>'

        res = posts.update(blogId=blog_id, postId=post_id, body=body).execute()
        print('업데이트 완료')

    except client.AccessTokenRefreshError:
        print(
            "The credentials have been revoked or expired, please re-run"
            "the application to re-authorize"
        )


def extract_robotable_link_and_title(post_url: str, naver_id: str) -> str:
    robotable_url = 'https://blog.naver.com' + \
                    BeautifulSoup(requests.get(post_url).content, features='lxml').select_one('iframe')['src']
    title = BeautifulSoup(requests.get(robotable_url).content, features='lxml').select_one('title').string

    return robotable_url, title


def init(argv) -> tuple:
    # Authenticate and construct service.
    _service, _flags = sample_tools.init(
        '',
        "blogger",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/blogger",
    )
    _posts = _service.posts()

    with open('settings.json', encoding='utf-8') as f:
        settings = json.load(f)
        _naver_id = str(settings['naverID'])
        _blog_id = str(settings['blogID'])
        _post_id = str(settings['postID'])

    return _naver_id, _blog_id, _post_id, _service


def test():
    print()


if __name__ == "__main__":
    test()
    __naver_id, __blog_id, __post_id, __service = init(sys.argv)
    __posts = __service.posts()
    print('Q를 입력할 때까지 계속 입력할 수 있습니다')

    while True:
        print('옵션이나 포스트 URL을 입력하세요: ', end='')
        input_data = input()

        if input_data.upper() == 'Q':
            __service.close()
            break
        else:
            _link, _title = extract_robotable_link_and_title(input_data, naver_id=__naver_id)
            poster(_link, _title, posts=__posts)
