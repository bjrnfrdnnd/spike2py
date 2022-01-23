from enum import Enum


class EnumChannelTypes(Enum):
    EVENTS = 'events'
    KEYBOARD = 'keyboard'
    WAVEFORM = 'waveform'
    WAVEMARK = 'wavemark'
    UNSET = 'unset'
