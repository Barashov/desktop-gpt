# Desktop file transribe
## configure:
```shell
python -m venv venv
```
linux:
```shell
source venv/bin/activate
```
windows:
```shell
venv\Scripts\activate
```
install requirements
```shell
pip install -r requirements.txt 
```
## use
transcribe all audio and video files
in folder
```shell
python main.py
```

parameters:
- filename
- prompt
- temperature
- language
- response_format

how use:
```shell
python main.py filename=file.mp3 temperature=1
```

.env:
```
OPENAI_API_KEY=<API-KEY>
```
