# Project Setup

以下の手順で環境を設定し、コードを実行してください。

## 注意点
- slack-bot.pyのOpenAIのAPIキー、SlackのAPIトークンは自分のものに置き換えてください。
- SLACK_CHANNELSに投稿先チャンネル名を設定してください。
- Slackチャンネルにアプリの追加も忘れずに行ってください。

## 環境設定手順

### venv用仮想環境を作成する:

```bash
git clone https://github.com/jpwstu/MySlackBot_for_papers.git
cd MySlackBot_for_papers
code .
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python slack-bot.py
```

### docker用仮想環境を作成する:

```bash
docker-compose up -d
docker-compose exec slack-bot sh
cd slackbot
python slack-bot.py
```