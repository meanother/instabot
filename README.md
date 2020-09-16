# instabot

### Download chromedriver:
https://chromedriver.chromium.org/downloads


### Initialize
```shell script
cd $HOME ; \
git clone https://github.com/meanother/instabot.git ; \
cd instabot ; \
python3 -m venv env ; \
source env/bin/activate ; \
pip install -r requirments.txt ; \
echo "login='YOUR_LOGIN'\npassword='YOUR_PASSWORD'" > $HOME/instabot/service/settings.py
```

### Settings
Copy chromedriver to /service/
Please enter the list of hashtags you need in the file: hashtags.txt  
example:  
    vsco  
    followme  
    art  


### Run
```shell script
python $HOME/instabot/service/bot.py
```

