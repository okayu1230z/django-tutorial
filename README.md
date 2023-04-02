# django-tutorial

https://www.djangoproject.com/ のチュートリアルをやってみる

ここからは https://docs.djangoproject.com/ja/4.1/intro/tutorial03/

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

## ビューを追加

`polls/template/polls/index.html`

```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li>
            <!-- <a href="/polls/{{ question.id }}/">{{ question.question_text }}</a> -->
            <!-- 下記のように書くとハードコードが削除される -->
            <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

`polls/views.py`

```python
...

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```
