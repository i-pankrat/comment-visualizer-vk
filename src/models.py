import requests

import torch
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

class NeuralNetworkmanager:
    def __init__(self):
        self.translator_is_init = False
        self.converter_model_is_init = False
        self.image_converter_model = "runwayml/stable-diffusion-v1-5"

    def __initizlize_translator__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        self.translator_is_init = True

    def __initialize_image_converter__(self, device):
        if device == "cuda" and not torch.cuda.is_available():
            raise Exception("Your device does not support cuda :(")

        self.device = device
        self.image_converter = StableDiffusionPipeline.from_pretrained(self.image_converter_model).to(self.device)
        self.converter_model_is_init = True

    def convert_image(self, text, device, save_name, steps, height, width):
        if not self.converter_model_is_init or self.device != device:
            self.__initialize_image_converter__(device)

        image = self.image_converter(prompt=text, num_inference_steps=steps, height=height, width=width).images[0]
        image.save(f"{save_name}")

    def translate(self, text):
        if not self.translator_is_init:
            self.__initizlize_translator__()

        batch = self.tokenizer([text], truncation=True, max_length=60, return_tensors="pt")
        generated_ids = self.translate_model.generate(**batch, max_length=60)
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
