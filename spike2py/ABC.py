from __future__ import annotations

import pathlib
import typing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Union

import numpy as np


class ChannelInfoA(ABC):
    pass


class ChannelA(ABC):

    @abstractmethod
    def __init__(self, channel_info: ChannelInfoA, times: np.ndarray) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_repr(cls, ch_type: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_channel_generator(cls, ch_type: str) -> ChannelA:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class TrialInfoA(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass


class TrialA(ABC):
    channel_dict: dict

    @abstractmethod
    def __init__(self, trial_info: TrialInfoA) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def get_short_channel_info(self) -> list:
        pass

    @abstractmethod
    def get_safe_path_pickle(self) -> pathlib.Path:
        pass

    @abstractmethod
    def _add_defaults_to_trial_info(self, trial_info: TrialInfoA):
        pass

    @abstractmethod
    def _parse_trial_data(self):
        pass

    @abstractmethod
    def _import_trial_data(self) -> ChannelA:
        pass

    @abstractmethod
    def plot(self, save: Literal[True, False] = None) -> None:
        pass

    @abstractmethod
    def save(self, file: typing.Optional[Union[Path, str]] = None):
        pass
