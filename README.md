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

```python
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
```

reverseは名前からurlを呼び出すときに利用する

reverse('name')とすると、urls.pyのurlpatternsで指定したnameで呼び出せる

results.html

```html
<h1>{{ question.question_test }}</h1>

<ul>
    {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
    {% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

元々この記述だったurls.pyが

```python
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'), # /polls/
    path('<int:question_id>/', views.detail, name='detail'), # /polls/5/
    path('<int:question_id>/results/', views.results, name='results'), # /polls/5/results/
    path('<int:question_id>/vote/', views.vote, name='vote'), # /polls/5/vote/
]
```

汎用ビューを使うとこうなる

