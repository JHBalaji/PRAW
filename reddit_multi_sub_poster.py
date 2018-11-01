import praw
import time
import re

_pattern = re.compile('again in (?P<number>[0-9]+) (?P<unit>\w+)s.?', re.IGNORECASE)

def handle_rate_limit(exc):
    time_map = {
        'second': 1,
        'minute': 60,
        'hour': 60 * 60,
    }
    matches = _pattern.findall(exc.message)
    delay = int(matches[0][0]) * time_map[matches[0][1]]
    time.sleep(delay + 1)

sub_reddit_names = [''] #these are the subreddit you are posting to.

post_title = ''  # this is the post title
post_body = ''  # this is the post text/body


# Here we create a reddit instance. We make an object with our credentials to work with the PRAW API.
# you originally had r but /u/bboe (the author of PRAW) recommends using 'reddit' for readability purposes
# but you can use whatever you want.
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password=',
    user_agent='')


def authenticate(reddit):
    # API uses lazy loading so everytime you request, it 'logs in' to verify you are logged in, call the me() function
    # to verify that the credentials you provided do work.
    print(reddit.user.me())

def self_post(sub_reddit):
    # using the documentation, we can see that using the reddit object we created we can access the subreddit module
    # provide the desired subreddit we want to post, and then call the submit method which you can provide the
    # parameters you want. In this demo, I provided keyword=argument

    # this is where you reference the sub_reddit variable with is 'test' as well as the post title and post body.
    # You can directly substitute sub_reddit with 'test', you can substitute title=post_post title with title="test post",
    # and finally you can substitute selftext=post_body with selftext='my body/text'
    reddit.subreddit(sub_reddit).submit(title=post_title, selftext=post_body)

# to circumvent rate_limiter posed by sub moderators. Reddit sub ratelimit is defined in sub level irrespective of karma
while True:
    authenticate(reddit)
    try:
        list(map(lambda _: self_post(_), sub_reddit_names))
        break
    except praw.exceptions.APIException as e:
        if e.error_type == 'RATELIMIT':
            handle_rate_limit(e)
        else:
            raise


