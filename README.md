# django-tutorial

https://www.djangoproject.com/ のチュートリアルをやってみる

ここは[インストール方法](https://docs.djangoproject.com/ja/4.1/intro/tutorial01/)のdemo

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

## 初めてのビュー作成

```
$ docker exec -it django-app bash
# cd app/mysite
~/app/mysite# python manage.py startapp polls
~/app/mysite# ls polls/
__init__.py  admin.py  apps.py	migrations  models.py  tests.py  views.py
~/app/mysite# python manage.py runserver 0.0.0.0:8000
```

`http://localhost:8000/polls/` にアクセスすると「Hello, world. You're at the polls index.」が表示される

## path()

- route: URLパターン
- view: 呼び出されるビュー関数
- kwargs: 任意のキーワード引数を辞書として対象のビューに渡せる
- name: URLに名前付けが可能。Djangoの中から参照できる。テンプレートの中で有効