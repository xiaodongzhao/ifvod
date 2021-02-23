# ifvod

Script to download videos from https://www.ifvod.tv/, using selenium and Firefox.

## install
```
pip install selenium-wire
pip install selenium
```

Download [geckodriver](https://github.com/mozilla/geckodriver/releases/)
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
tar -xvzf geckodriver-v0.29.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
```
Install FFmpeg
```
sudo apt install ffmpeg
```

## run 
```
python ifvod.py https://www.ifvod.tv/detail\?id\=gmN3PuozDET
```
