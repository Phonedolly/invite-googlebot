import json
from google.auth.transport.requests import AuthorizedSession
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPE = 'https://www.googleapis.com/auth/blogger'


def init() -> AuthorizedSession:
    flow = InstalledAppFlow.from_client_secrets_file('./client_secrets.json', scopes=[SCOPE])
    flow.run_local_server()
    return flow.authorized_session()


def task_post(session: AuthorizedSession) -> None:
    print("Input New Post URL: ", end='')
    newURL = input()

    blogID = None
    postID = None

    with open('settings.json', encoding='utf-8') as f:
        settings = json.load(f)
        blogID = str(settings['blogID'])
        postID = str(settings['postID'])

    res = session.get('https://www.googleapis.com/blogger/v3/blogs/' + blogID + '/posts/' + postID)
    body = json.loads(res.content.decode('utf-8'))
    body['content'] = \
        body['content'] \
        + '<br><a href="' + newURL + '">' + newURL + '&nbsp;</a>'  # 문자열을 읽을 때에는 json.loads()를 사용한다

    session.put(url='https://www.googleapis.com/blogger/v3/blogs/' + blogID + '/posts/' + postID, data=body)

    print()


# <a href="https://hello220807.blogspot.com/2022/08/useful-links.html">https://hello220807.blogspot.com/2022/08/useful-links.html&nbsp;</a>

if __name__ == '__main__':
    _session = init()
    task_post(_session)
    _session.close()
