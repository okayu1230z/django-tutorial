FROM python:3
USER root

# 環境のセットアップ
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# 作業ツールのインストール（デプロイ用Imageでは抜くこと）
RUN apt-get install -y vim less

# pipのインストール
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# アプリケーション依存パッケージのインストール
RUN python -m pip install Django

# ポート開放
EXPOSE 8000
