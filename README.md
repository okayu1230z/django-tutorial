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

## Databaseの設定

データベースの設定は　`mysite/settings.py`　にある

- ENGINE: `django.db.backends.sqlite3`や`django.db.backend.postgresql`などを指定する
- NAME: データベースの名前で、SQLiteを使用している場合はコンピュータ上のファイルを指定する

データベースとしてSQLiteを使っていない場合、USER、PASSWORD、HOSTなどの設定を追加する必要がある。


TIME_ZONE でタイムゾーンの設定ができる

INSTALLED_APPS にデフォルトで入っているアプリケーションは以下の通り

```
INSTALLED_APPS = [
    'django.contrib.admin', // 管理サイト
    'django.contrib.auth', // 認証システム
    'django.contrib.contenttypes', // コンテンツタイプフレームワーク
    'django.contrib.sessions', // セッションフレームワーク
    'django.contrib.messages', // メッセージフレームワーク
    'django.contrib.staticfiles', // 静的ファイルの管理フレームワーク
]
```

これらの機能はよく使われるのでデフォルトで付属していて、最低1つのデータベーステーブルを使うので、使い始める前にデータベースにテーブルを作る必要がある

```
$ docker exec -it django-app bash
# cd app/mysite
# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
# sqlite3 app/mysite/
db.sqlite3  manage.py   mysite/     polls/      
# sqlite3 app/mysite/db.sqlite3 
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> 
```

sqlite3コマンドが入っている場合はホストマシンでも実ファイルを指定してsqlite3を実行できる

```
$ which sqlite3
/usr/bin/sqlite3
$ sqlite3 app/mysite/db.sqlite3 
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .table
auth_group                  auth_user_user_permissions
auth_group_permissions      django_admin_log          
auth_permission             django_content_type       
auth_user                   django_migrations         
auth_user_groups            django_session
```

## モデルの作成

モデルは本質的にはデータベースレイアウトとそれに付随するメタデータのこと

rorと違ってマイグレーションは完全にモデルのファイルから生成される

QuesttionとChoiceの2つのモデルを作成する

Pollにはquestionとpublication dateの情報がある。Choiceには選択肢のテキストとvoteという2つのフィールドがある。各Choiceは1つのQuestionに関連づけられている

`polls/models.py` に下記のように記述

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200) # CharField は文字フィールド
    pub_date = models.DateTimeField('date published') # DateTimeField は日時フィールド

class Choice(modesl.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCASE) # Choiceが1つのQuestionに関連づけられることを定義している
    choice_text = models.CharField(max_length=200) # CharField にはmex_lengthが必須項目
    votes = models.IntergerField(default=0)
```

各モデルは1つのクラスで表現され、いずれも`django.db.models.Model`のサブクラス

各モデルには複数のクラス変数があり、個々のクラス変数はモデルのデータベースフィールドを表現している

アプリケーションをプロジェクトに含めるには、構成クラスへの参照をINSTALLED_APPS設定に追加する必要がある

PollsConfigクラスはpolls/apps.pyにあるので、ドット繋ぎのパスは`polls.apps.PollsConfig`となる

```
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

この記述でDjangoがpollsアプリケーションに認識できるようになる

`makemigrations`を実行することでDjangoにモデルに変更があったことを伝え、そして変更をマイグレーションの形で保存することができる。

```
$ python manage.py makemigrations polls
Migrations for 'polls':
  polls/migrations/0001_initial.py
    - Create model Question
    - Create model Choice
```

マイグレーションはディスク上のただのファイル（`polls/migrations/0001_initial.py`）

Djangoにはマイグレーションをあなたの代わりに実行し、自動でデータベーススキーマを管理するための`migrate`コマンドがある

`sqlmigrate`コマンドはマイグレーションの名前を引数に取ってSQLを返す。
このコマンドは実査にはマイグレーションを実行しない。
Djangoが必要としているSQLが何であるかをスクリーンに表示するだけ。

```
# python manage.py sqlmigrate polls 0001
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
```

`check`コマンドを実行するとマイグレーションを作成したりデータベースに触れることなくプロジェクトに何か問題がないか確認できる

```bash
# python manage.py check
System check identified no issues (0 silenced).
```

実際にマイグレーションするには以下のコマンドを実行する


```bash
# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Applying polls.0001_initial... OK
```

## APIで遊ぶ

```
# python manage.py shell
Python 3.11.2 (main, Mar 23 2023, 14:09:52) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2023, 4, 2, 9, 3, 2, 811376, tzinfo=datetime.timezone.utc)
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

`Qeustion: Question object(1)`というのはオブジェクトの表現としては役に立たない

`polls/models.py`ファイル内にあるQuestionモデルの`__str__()`メソッドをQuestionとChoiceの両方に追加する

```
class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```

Qeustionにはさらに`was_published_recently`関数を追加する

```
class Question(models.Model):
    question_text = models.CharField(max_length=200) # CharField は文字フィールド
    pub_date = models.DateTimeField('date published') # DateTimeField は日時フィールド

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

再び遊ぶ

```
# python manage.py shell
Python 3.11.2 (main, Mar 23 2023, 14:09:52) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from polls.models import Choice, Question
>>> Question.object.all()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: type object 'Question' has no attribute 'object'
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>
```

もうちょっと遊ぶ

```
# python manage.py shell
Python 3.11.2 (main, Mar 23 2023, 14:09:52) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from polls.models import Choice, Question
>>> Question.objects.get(pk=1)
<Question: What's up?>
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True
>>> q.choice_set.all()
<QuerySet []>
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question
<Question: What's up?>
>>> from django.utils import timezone
>>> Choice.objects.filter(question__pub_date__year=timezone.now().year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
(1, {'polls.Choice': 1})
>>> q.choice_set.count()
2
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>]>
```
