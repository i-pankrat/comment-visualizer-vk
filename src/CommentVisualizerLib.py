from utils import parse_post_link
from models import NeuralNetworkmanager, VKAPI, KeyWordsGetter
from config import secret_key, vk_api_version

# models
vk = VKAPI(access_token=secret_key, version=vk_api_version)
neural_networks = NeuralNetworkmanager()
kw_getter = KeyWordsGetter()

def get_comments_from_json(comments_json):
    comments = []
    for comment in comments_json['response']['items']:
        text = comment['text'].replace("\n", "")
        comments.append(text)

    return ", ".join(comments)

def generate_image(post_url, device, file_name, steps, height, width):
    global vk, neural_networks, kw_getter

    # Send VK API request
    owner_id, post_id = parse_post_link(post_url)
    params = {'owner_id': owner_id, 'post_id': post_id}
    response = vk.get_comments(params)

    # Process JsonResponse
    if "response" in response:
        comments = get_comments_from_json(response)
    else:
        raise Exception(response['error']['error_msg'])
    if not comments:
        raise Exception("Post has zero comments :(")

    # Process result
    key_words = kw_getter.get(comments, collocation_size=1)
    en_text = neural_networks.translate(key_words)

    # Generate image
    neural_networks.convert_image(en_text, device, file_name, steps, height, width)
