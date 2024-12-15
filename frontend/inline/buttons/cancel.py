from inline.callback.callbacks import (
    CALL_OFF_CALLBACK,
    REFUSAL_TO_DESCRIBE_CALLBACK,
    CB,
)
from inline.callback.constants import (
    CALL_OFF_OUTPUT,
    REFUSAL_TO_DESCRIBE_OUTPUT,
)
from .types import Button


def get_home_btn(output=CALL_OFF_OUTPUT) -> Button:
    return {output: {CB: CALL_OFF_CALLBACK}}


def get_refusal_to_describe_btn() -> Button:
    return {REFUSAL_TO_DESCRIBE_OUTPUT: {CB: REFUSAL_TO_DESCRIBE_CALLBACK}}
