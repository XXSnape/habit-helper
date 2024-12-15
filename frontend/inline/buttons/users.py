from .types import Button

from inline.callback.callbacks import CB
from inline.callback.constants import FREEZE_OUTPUT, DEFROST_OUTPUT
from inline.callback.factories import activity_user_factory


def get_freezing_or_defrosting_btn(is_active: bool) -> Button:
    output = FREEZE_OUTPUT if is_active else DEFROST_OUTPUT
    return {output: {CB: activity_user_factory.new(is_active=int(not is_active))}}
