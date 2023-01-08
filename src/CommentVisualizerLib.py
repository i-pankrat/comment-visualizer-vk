from utils import parse_post_link
from models import NeuralNetworkManager, VKAPI, KeyWordsGetter
from config import VK_ACCESS_TOKEN, vk_api_version


def get_comments_from_json(comments_json):
    comments = []
    for comment in comments_json["response"]["items"]:
        text = comment["text"].replace("\n", "")
        comments.append(text)

    return ", ".join(comments)


class CommentVisualizer:
    def __init__(self):
        self.vkapi = VKAPI(access_token=VK_ACCESS_TOKEN, version=vk_api_version)
        self.neural_networks = NeuralNetworkManager()
        self.kw_getter = KeyWordsGetter()

    def generate_image(self, post_url, device, steps, height, width):

        # Send VK API request
        owner_id, post_id = parse_post_link(post_url)
        params = {"owner_id": owner_id, "post_id": post_id}
        response = self.vkapi.get_comments(params)

        # Process JsonResponse
        if "response" in response:
            comments = get_comments_from_json(response)
        else:
            raise Exception(response["error"]["error_msg"])
        if not comments:
            raise Exception("Post has zero comments :(")

        # Process result
        key_words = self.kw_getter.get(comments, collocation_size=1)
        en_text = self.neural_networks.translate(key_words)

        # Generate image
        self.neural_networks.set_device = device
        return self.neural_networks.convert_image(en_text, steps, height, width)
