# 使用するベースイメージを指定
FROM python:3.10-alpine3.18

# 環境変数を設定する
ENV PYTHONUNBUFFERED=1

# ワーキングディレクトリを設定する
WORKDIR /app

# 必要なシステムパッケージをインストールする
RUN apk update && apk add --no-cache gcc musl-dev

# requirements.txtをコピーする
COPY requirements.txt /app/

# Pythonパッケージをインストールする
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app