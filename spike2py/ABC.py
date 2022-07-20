from __future__ import annotations

import pathlib
import typing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Union, Optional

import numpy as np

from spike2py.enums import EnumChannelTypes
from spike2py.types import (
    # parsed_wavemark,
    parsed_waveform,
    # parsed_event,
    # parsed_keyboard,
)


class ChannelInfoA(ABC):
    name: str = None
    units: str = None
    comment: str = None
    sampling_frequency: int = None
    path_save_figures: Path = None
    trial_name: str = None
    subject_id: str = None
    pass


class ChannelA(ABC):

    @abstractmethod
    def __init__(self, channel_info: ChannelInfoA, times: np.ndarray) -> None:
        self.times = times
        self.channel_info = channel_info
        self.info = channel_info
        self.times = times
        self.values = np.array([])
        self.raw_values = self.values
        self.path_save_figures: Optional[Path] = None
        self.type = EnumChannelTypes.UNSET.value
        self.name: Optional[str] = channel_info.name

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

    @abstractmethod
    def __init__(self, trial_info: TrialInfoA) -> None:
        self.trial_info = trial_info
        self.channel_dict: dict = {}
        self.info = trial_info
        self._add_defaults_to_trial_info(trial_info)
        self._parse_trial_data()
        self.name = None

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


class WaveformA(ChannelA):

    @abstractmethod
    def __init__(self, name: str, data_dict: parsed_waveform) -> None:
        self.data_dict = data_dict
        self.name = name

    @abstractmethod
    def plot(self, save: Literal[True, False] = None) -> WaveformA:
        pass
