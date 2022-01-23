from enum import Enum


class EnumChannelTypes(Enum):
    EVENT = 'event'
    KEYBOARD = 'keyboard'
    WAVEFORM = 'waveform'
    WAVEMARK = 'wavemark'
    UNSET = 'unset'
