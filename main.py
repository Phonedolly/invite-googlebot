from __future__ import print_function

__author__ = "jcgregorio@google.com (Joe Gregorio)"

import json
import sys

from oauth2client import client
from googleapiclient import sample_tools

SCOPE = 'https://www.googleapis.com/auth/blogger'


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv,
        "blogger",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/blogger",
    )

    try:
        posts = service.posts()

        print("Input New Post URL: ", end='')
        new_url = input()

        blog_id = None
        post_id = None

        with open('settings.json', encoding='utf-8') as f:
            settings = json.load(f)
            blog_id = str(settings['blogID'])
            post_id = str(settings['postID'])

        body = posts.get(blogId=blog_id, postId=post_id).execute()
        body['content'] = body['content'] \
                          + '<br><a href="' + new_url + '">' + new_url + '&nbsp;</a>'  # 문자열을 읽을 때에는 json.loads()를 사용한다

        res = posts.update(blogId=blog_id, postId=post_id, body=body).execute()
        print(res)

    except client.AccessTokenRefreshError:
        print(
            "The credentials have been revoked or expired, please re-run"
            "the application to re-authorize"
        )


if __name__ == "__main__":
    main(sys.argv)
