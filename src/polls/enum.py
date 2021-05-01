import enum
from django.utils.translation import gettext_lazy as _


class TypePoll(enum.Enum):
    text = 'text'
    choice = 'choice'
    multiple_choice = 'multiple choice'


typePollChoices = (
    (TypePoll.text.value, _('text')),
    (TypePoll.choice.value, _('choice')),
    (TypePoll.multiple_choice.value, _('multiple choice'))
)
