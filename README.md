# Tgbot_bpm22-1
This Telegram bot is designed for use by university students of my group to help manage their classes and stay connected with their classmates. The bot is built using Python and the python-telegram-bot API.

### Features
The University Telegram Bot has the following features:

- Schedule: View class schedules for the tommorow, current day, week.
- Homework: Get updates on upcoming homework assignments.
- Group Members: View a list of all members in the group and their contact information.
- Stuff: List of all links that will help you on the road.

---

## Installation
- Clone the repository to your local machine:
```
git clone https://github.com/your_username/university-telegram-bot.git
```
- Install the required packages:
```
- pip install -r requirements.txt
```
- Create a new bot on Telegram and obtain the bot token.
- Update the ```telegram_token_example.py``` file with your bot token
- Update the following lines in bot.py with path to ```db``` and ```stuff``` folders
```
sys.path.insert
```
- Run the bot using the following command:
```
python bot.py
```

---
## Usage
Once the bot is running, you can interact with it using the following commands and buttons:

- /schedule: View class schedules.
- /homework: Get updates on upcoming homework assignments.
- /group: View a list of all members in the group and their contact information.
- /links: Links to some useful stuff.

---
## Contributing
If you would like to contribute to this project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix:

```
git checkout -b my-new-feature
```
- Make your changes and commit them:
```
git commit -am 'Add some feature'
```
- Push your changes to your forked repository:
```
git push origin my-new-feature
```
- Create a new pull request.
