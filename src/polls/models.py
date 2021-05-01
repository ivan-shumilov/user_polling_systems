from django.db import models
from django.utils.translation import gettext_lazy as _
from .validates import validateQuestionType
from .enum import typePollChoices


class SortingField(models.Model):
    sorting = models.PositiveIntegerField(verbose_name=_('sorting'), default=0)

    class Meta(object):
        abstract = True


class Poll(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'))
    date_start = models.DateTimeField(verbose_name=_('date start'))
    date_finish = models.DateTimeField(verbose_name=_('date finish'))

    class Meta:
        verbose_name_plural = _('polls')
        verbose_name = _('poll')
        app_label = 'polls'
        ordering = ('-date_start',)

    def __str__(self):
        return self.name


class Question(SortingField):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'), on_delete=models.CASCADE)
    question_text = models.TextField(verbose_name=_('question text'))
    question_type = models.CharField(verbose_name=_('question type'), max_length=50, choices=typePollChoices,
                                     validators=[validateQuestionType])

    class Meta:
        verbose_name_plural = _('questions')
        verbose_name = _('question')
        app_label = 'polls'
        ordering = ('sorting',)

    def __str__(self):
        return self.question_text


class OptionTheQuestion(SortingField):
    question = models.ForeignKey(Question, verbose_name=_('question'), on_delete=models.CASCADE)
    option_text = models.TextField(verbose_name=_('option text'))
    option_true = models.BooleanField(verbose_name=_('option true'), default=False)

    class Meta:
        verbose_name_plural = _('options the questions')
        verbose_name = _('option the question')
        app_label = 'polls'
        ordering = ('sorting',)

    def __str__(self):
        return self.question_text


class CompletedPoll(models.Model):
    user_id = models.IntegerField(verbose_name=_('user id'))
    poll = models.ForeignKey(Poll, verbose_name=_('poll'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name_plural = _('completed polls')
        verbose_name = _('completed poll')
        app_label = 'polls'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.poll.name} was completed by {self.user_id}'


class UserAnswer(models.Model):
    completed_poll = models.ForeignKey(CompletedPoll, verbose_name=_('completed poll'), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_('question'), on_delete=models.CASCADE)
    answer = models.TextField(verbose_name=_('answer'))

    class Meta:
        verbose_name_plural = _('user answers')
        verbose_name = _('user answer')
        app_label = 'polls'
        ordering = ('id',)

    def __str__(self):
        return self.answer
