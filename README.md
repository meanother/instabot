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
pip install -r requirments.txt
```
### example: HASHTAGS.TXT  
vsco  
заебись  
nike  
followme   


### Example run, change to your parameters
```shell script
source $HOME/instabot/env/bin/activate/ ; \
python $HOME/instabot/service/bot.py \
--login="YOUR_LOGIN" \
--password="YOUR_PASSWORD" \
--path="PATH/TO/HASHTAGS.TXT" \
--chromedriver="/usr/local/chromedriver" \
--like="Like"
```

