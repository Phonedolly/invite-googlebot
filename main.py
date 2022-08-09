import json

from oauth2client import client
from googleapiclient import sample_tools

SCOPE = 'https://www.googleapis.com/auth/blogger'


def poster(robotable_url: str, posts):
    try:
        with open('settings.json', encoding='utf-8') as f:
            settings = json.load(f)
            blog_id = str(settings['blogID'])
            post_id = str(settings['postID'])

        body = posts.get(blogId=blog_id, postId=post_id).execute()
        body['content'] = body['content'] + '<br><a href="' + robotable_url + '">' + robotable_url + '</a>'

        res = posts.update(blogId=blog_id, postId=post_id, body=body).execute()
        print('업데이트 완료')

    except client.AccessTokenRefreshError:
        print(
            "The credentials have been revoked or expired, please re-run"
            "the application to re-authorize"
        )


def extract_robotable_link(post_url: str, naver_id: str) -> str:
    _post_id = post_url[post_url.rfind('/') + 1:]
    return 'https://blog.naver.com/PostView.naver?blogId=' + naver_id + '&logNo=' \
           + _post_id + '&redirect=Dlog&widgetTypeCall=true&directAccess=false'


def init() -> tuple:
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


if __name__ == "__main__":
    __naver_id, __blog_id, __post_id, __service = init()

    print('Q를 입력할 때까지 계속 입력할 수 있습니다')

    while True:
        print('옵션이나 포스트 URL을 입력하세요: ', end='')
        input_data = input()

        if input_data.upper() == 'Q':
            __service.close()
            break
        else:
            poster(extract_robotable_link(input_data, naver_id=__naver_id), posts=__service.posts())
