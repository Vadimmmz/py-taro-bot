# PyTaroBot
A telegram bot that makes predictions on a given topic using a three-card tarot layout. 


## About this app

**Don't execute this script more than one time!** Because it will break you settings.yaml file.

[TaroBot](https://github.com/pamnard/TaroBot)

## How to install


```bash
cd /home
git clone https://link
python -m venv env

# Activate virtual environment for Windows
source env/Scripts/activate

# Activate virtual environment fo for Linux
source env/bin/activate

# install all the libraries that are needed to work
pip install -r requirements.txt

deactivate

# Add .env file
echo 'OPENAI_API_KEY="PUT_OPENAI_API_KEY_HERE"' > .env && echo 'TELEGRAM_TOKEN="PUT_TELEGRAM_TOKEN_HERE"' >> .env

# Making a service for bot
sudo cp /home/py-taro-bot/py-taro-bot.service /lib/systemd/system/py-taro-bot.service

sudo systemctl enable py-taro-bot.service
sudo systemctl start py-taro-bot.service
```

## Used packages
This libraries was used:
- pyTelegramBotAPI==4.16.1
- openai==1.13.3
- python-dotenv==1.0.1

## License

MIT License