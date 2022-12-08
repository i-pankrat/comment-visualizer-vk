# comment-visualizer-vk

How to launch:

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
6. Insert your personal or service token in config.py
7. Start the application!
``` shell
cd src/
streamlit run steamlit_app.py
```