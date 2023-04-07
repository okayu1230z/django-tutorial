# django-tutorial

https://www.djangoproject.com/ のチュートリアルをやってみる

ここからは　https://docs.djangoproject.com/ja/4.1/intro/tutorial05/

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

# 自動テストの導入

テストのないコードはデザインとは壊れている by Jacob Kaplan-Moss

```
$ docker exec -it django-app bash
# cd app/mysite; python manage.py shell
Python 3.11.3 (main, Apr  5 2023, 22:58:06) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> future_question = Question(pub_date=timezone.now()+datetime.timedelta(days=30))
>>> future_question.was_published_recently()
True
```

以上のように未来の時間でも最近publishされた判定になるバグが存在する

バグをあぶりだすためにテストを追加する

```
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

未来の日付のpub_dateを持つQuestionのインスタンスを生成するメソッドを持つdjango.test.TestCaseを継承したサブクラスを作っている

それからwas_published_recently()の出力をチェックしていて、これはFalseになることが想定されているはず

```
# python manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionModelTests.test_was_published_recently_with_future_question)
was_published_recently() returns False for questions whose pub_date
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/root/app/mysite/polls/tests.py", line 18, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

`python manage.py test polls`はpollsアプリケーション内にある`django.taet.TestCase`クラスのサブクラスを探す

テストを通るように修正すれば下記のような結果になる

```
# python manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Destroying test database for alias 'default'...
```

## Viewのテスト

Viewに対するテスト

```
# python manage.py shell
Python 3.11.3 (main, Apr  5 2023, 22:58:06) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
>>> from django.test import Client
>>> client = Client()
>>> response = client.get('/')
Not Found: /
>>> response.status_code
404
>>> from django.urls import reverse
>>> response = client.get(reverse('polls:index'))
>>> response.status_code
200
>>> response.context['latest_question_list']
<QuerySet [<Question: What's up?>]
```

## Viewの改良

公開されていない投票（pub_dateの日付が未来になっている）が表示されないようにしたい

汎用ビューについて

https://codor.co.jp/django/generic-class-based-view-number

- LIST系
  - ListView
- DETAIL系
  - DetailView
- EDIT系
  - CreateView
  - DeleteView
  - UpdateView
  - FormView
- BASE系
  - TemplateView
  - View
  - RedirectView
- DATES系
  - ArchiveView
  - DateDetailView
  - Day,Month,Today,Week,Year ArchiveView
