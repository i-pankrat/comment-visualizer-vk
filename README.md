# About

The app takes a link to a VKontakte post and visualizes its comments using a model from [Hugging Face](https://huggingface.co/).

# Run tests

``` shell
python -m tests.utilsTests
```

# How to launch:

1. Clone reopsiroty
``` shell
git clone https://github.com/i-pankrat/comment-visualizer-vk
```
2. Create venv
``` shell
cd comment-visualizer-vk
python -m venv venv
. venv/bin/activate
```
3. Install requirements
``` shell
pip install -r requirements.txt
```
4. Install [torch](https://pytorch.org/)
5. Log to hugging faces
``` shell
huggingface-cli login
```
6. Add your vk access token to your environment variable. Create an application in vk to get the access token. You can create app [here](https://vk.com/editapp?act=create). Then go to setttings of the created app and find the 'Service token' there. That's what you need to put insted of YOUR_ACESS_TOKEN in the command below.
``` shell
export VK_ACCESS_TOKEN=YOUR_ACESS_TOKEN
```
7. Start the application!
``` shell
cd src/
streamlit run steamlit_app.py
```