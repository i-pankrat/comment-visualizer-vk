import re

def parse_post_link(url):
    pattern_text = r'\s*https://vk.com/(?P<domain>\S+)\?w=wall(?P<owner_id>\S+)_(?P<post_id>\d+)[%2Fall]?\s*'
    pattern = re.compile(pattern=pattern_text)
    match = pattern.match(url)

    if not match:
        raise Exception("Bad post link")

    owner_id = match.group('owner_id')
    post_id = match.group('post_id')
    return owner_id, post_id
