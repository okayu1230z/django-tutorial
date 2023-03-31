# django-tutorial

https://www.djangoproject.com/ のチュートリアルをやってみる

ここは　https://docs.djangoproject.com/ja/4.1/intro/install/　のdemo

# 実行方法

docker containerを立ち上げる

```bash
$ docker-compose up
[+] Running 1/0
 ⠿ Container python3  Recreated                                                                                                                                        0.1s
Attaching to app
app  | Python 3.11.2 (main, Mar 23 2023, 14:09:52) [GCC 10.2.1 20210110] on linux
app  | Type "help", "copyright", "credits" or "license" for more information.
...
```

# 遊ぶ

## プロジェクト作成

コンテナの中に入ってプロジェクトを作成する

```
$ docker exec -it django-app bash
# python -V
Python 3.11.2
# python -m django --version
4.1.7
# cd app
# django-admin startproject mysite
```

これでdjangoのアプリケーションに必要なファイルが作成される

```
# ls mysite
manage.py mysite
# ls mysite/mysite/
__init__.py  asgi.py  settings.py  urls.py  wsgi.py
```

- manage.py: Djangoプロジェクトで様々な操作を行うためのコマンドラインユーティリティ
- asgi.py: Djangoプロジェクトを提供するASGI互換Webサーバのエントリポイント
- settings.py: Djangoプロジェクトの設定ファイル
- urls.py: DjangoプロジェクトのURL宣言を行うファイル
- wsgi.py: DjangoプロジェクトをserveするためのWSGI互換Webサーバとのエントリポイント

## 開発用サーバの起動

```
# python mysite/manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
March 31, 2023 - 09:55:08
Django version 4.1.7, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

手元のブラウザでlocalhost:8000見てみるとDjangoが立ち上がっているはず

開発サーバはPythonコードを自動的にリロードするらしい。便利。

## Pollsアプリケーションを作る

```
# python manage.py startapp polls
# ls -al polls/
合計 20
drwxr-xr-x 9 root root 288  3月 31 19:11 .
drwxr-xr-x 6 root root 192  3月 31 19:11 ..
-rw-r--r-- 1 root root   0  3月 31 19:11 __init__.py
-rw-r--r-- 1 root root  63  3月 31 19:11 admin.py
-rw-r--r-- 1 root root 142  3月 31 19:11 apps.py
drwxr-xr-x 3 root root  96  3月 31 19:11 migrations
-rw-r--r-- 1 root root  57  3月 31 19:11 models.py
-rw-r--r-- 1 root root  60  3月 31 19:11 tests.py
-rw-r--r-- 1 root root  63  3月 31 19:11 views.py
```

今回はここまで