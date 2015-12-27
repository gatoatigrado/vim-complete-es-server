import re


SPACES_RE = re.compile(ur'[^\w\d]+')


def get_all_words(s):
    words = SPACES_RE.split(s)
    words = (w.strip() for w in words)
    return [w for w in words if w]
