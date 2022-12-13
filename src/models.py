import requests

from torch import cuda
import spacy
from diffusers import StableDiffusionPipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textacy.extract.keyterms import sgrank

class VKAPI:
    def __init__(self, access_token, version):
        self.params = {'access_token': access_token, 'v': version}
        self.init_link = "https://api.vk.com/method"

    def method(self, method, params):
        url = self.add_method(method)
        params.update(self.params)
        response = requests.get(url, params)
        return response.json()

    def add_method (self, method):
        return self.init_link + "/" + method

    def get_wall(self, params):
        return  self.method('wall.get', params)

    def get_comments(self, params):
        return self.method('wall.getComments', params)

    def wall_search(self, params):
        return self.method('wall.search', params)

    def wall_get_by_id(self, params):
        return self.method('wall.getById', params)

class KeyWordsGetter:
    def __init__(self):
        self.spm = spacy.load("ru_core_news_sm")

    def get(self, text, collocation_size):
        return ", ".join([t for t, s in sgrank(self.spm(text), ngrams=collocation_size)])

class NeuralNetworkManager:
    def __init__(self):
        self.image_converter_model = "runwayml/stable-diffusion-v1-5"

        # Init ru-en text translator 
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")

        # Init image converter
        self.device = "cuda" if cuda.is_available() else "cpu"
        self.image_converter = StableDiffusionPipeline.from_pretrained(self.image_converter_model).to(self.device)

    def set_device(self, device):
        if self.device != device:
            self.device = device
            self.image_converter = self.image_converter.to(self.device)

    def convert_image(self, text, steps, height, width):
        return self.image_converter(prompt=text, num_inference_steps=steps, height=height, width=width).images[0]

    def translate(self, text):
        batch = self.tokenizer([text], truncation=True, max_length=60, return_tensors="pt")
        generated_ids = self.translate_model.generate(**batch, max_length=60)
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
