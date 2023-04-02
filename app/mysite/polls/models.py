import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200) # CharField は文字フィールド
    pub_date = models.DateTimeField('date published') # DateTimeField は日時フィールド

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Choiceが1つのQuestionに関連づけられることを定義している
    choice_text = models.CharField(max_length=200) # CharField にはmex_lengthが必須項目
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text