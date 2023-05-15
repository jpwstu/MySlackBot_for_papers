import os
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import arxiv
import openai
import random

# OpenAIのapiキー
openai.api_key = 'OPENAI_API_KEY'
# Slack APIトークン
SLACK_API_TOKEN = 'SLACK_API_TOKEN'
# Slackに投稿するチャンネル名を指定する(ここでは4つのチャンネルを指定)
SLACK_CHANNELS = ["#random-bot", "#generative-bot", "#cnn-bot", "#transformer-bot"]

def get_summary(result):
    system = """与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。```
    タイトルの日本語訳
    ・要点1
    ・要点2
    ・要点3
    ```"""

    text = f"title: {result.title}\nbody: {result.summary}"
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.25,
            )
    summary = response['choices'][0]['message']['content']
    title_en = result.title
    title, *body = summary.split('\n')
    body = '\n'.join(body)
    date_str = result.published.strftime("%Y-%m-%d %H:%M:%S")
    message = f"発行日: {date_str}\n{result.entry_id}\n{title_en}\n{title}\n{body}\n"
    
    return message

# arxiv APIで最新の論文情報を取得する
def search_arxiv(queries, num_papers = [3, 3, 3, 3]):
    '''
    queries: 検索クエリのリスト
    num_paper: 各クエリごとに取得する論文数
    '''
    
    results = {}
    for query in queries:
        search = arxiv.Search(
            query=query,  # 検索クエリ（
            max_results=100,  # 取得する論文数
            sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
            sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
        )
        #searchの結果を辞書に格納
        results[query] =  [result for result in search.results()]
        
        selected_papers = {}
        for query, num in zip(results.keys(), num_papers):
            selected_papers[query] = random.sample(results[query], k=num)
    return selected_papers

def main():
    # Slack APIクライアントを初期化する
    client = WebClient(token=SLACK_API_TOKEN)
    #queryを用意
    queries = ['ti:%22 Deep Learning %22', # random用
             'ti:%22 generative %22',
             'ti:%22 CNN %22',
             'ti:%22 Transformer %22']

    # arxiv APIで最新の論文情報を取得する
    selected_papers = search_arxiv(queries)
    
    # 論文情報をSlackに投稿する
    for channel, (query, papers) in zip(SLACK_CHANNELS, selected_papers.items()):
        for i, paper in enumerate(papers):
            try:
                # 今日の日付を取得
                today = datetime.now().strftime("%Y/%m/%d")
                # Slackに投稿するメッセージを組み立てる
                message = f"{today}の論文です！ {i+1}本目\n" + get_summary(paper)
                # Slackにメッセージを投稿する
                response = client.chat_postMessage(
                    channel=channel,
                    text=message
                )
                print(f"Message posted: {response['ts']}")
            except SlackApiError as e:
                print(f"Error posting message: {e}")
                
if __name__ == "__main__":
    main()