from django.core.exceptions import ValidationError
from .enum import TypePoll


def validateQuestionType(value):
    if value not in [TypePoll.text.value, TypePoll.choice.value, TypePoll.multiple_choice.value]:
        raise ValidationError('Invalid question type')
