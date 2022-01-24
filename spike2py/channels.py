from __future__ import annotations
import sys
from pathlib import Path
from typing import NamedTuple, Literal, Optional

import numpy as np

import spike2py.plot as plot
import spike2py.sig_proc as sig_proc
from spike2py.ABC import ChannelInfoA, ChannelA
from spike2py.enums import EnumChannelTypes

from spike2py.types import (
    parsed_wavemark,
    parsed_waveform,
    parsed_event,
    parsed_keyboard,
)

class ChannelInfoMeta(type(NamedTuple), type(ChannelInfoA)):
    pass

class ChannelInfo(NamedTuple, ChannelInfoA, metaclass=ChannelInfoMeta):
    """Information about channel

    See :class:`spike2py.channels.Channel` parameters for details.
    """

    name: str = None
    units: str = None
    sampling_frequency: int = None
    path_save_figures: Path = None
    trial_name: str = None
    subject_id: str = None


class Channel(ChannelA):
    """Base class for all channel types

    Parameters
     ----------
     channel_info
         name
             Name of channel (.e.g 'left biceps')
         units
             Units of recorded signal (e.g., 'Volts' or 'Nm')
         sampling_frequency
             In Hertz (e.g. 2048)
         path
             Defaults to path where data initially retrieved
         trialname
             Defaults to name of data file
         subject_id
             str indentifier
     times
         Sample times in seconds
    """

    def __init__(self, channel_info: ChannelInfo, times: np.ndarray) -> None:
        self.info = channel_info
        self.times = times
        self.values = np.array([])
        self.raw_values = self.values
        self.path_save_figures: Optional[Path] = None
        self.type = EnumChannelTypes.UNSET
        self.name: Optional[str] = channel_info.name

    @classmethod
    def get_channel_generator(cls, enm: EnumChannelTypes) -> Channel:
        thismodule = sys.modules[__name__]
        result = getattr(thismodule, enm.value.title())
        return result

    @classmethod
    def get_repr(cls, enm: EnumChannelTypes) -> str:
        result = f'{enm.value} channel'
        return result

    def __repr__(self) -> str:
        result = self.get_repr(enm=self.type)
        return result


class Event(Channel):
    """Event channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Event channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Event was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Event times in seconds
    """

    def __init__(self, name: str, data_dict: parsed_event) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                path_save_figures=data_dict.get("path_save_figures", None),
                trial_name=data_dict.get("trial_name", None),
                subject_id=data_dict.get("subject_id", None),
            ),
            data_dict.get("times", None),
        )
        self.type = EnumChannelTypes.EVENT

    def plot(self, save: Literal[True, False] = False) -> None:
        """Save Event channel figure

        Parameters
        ----------
        save
            Set to `True` to save Event figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self


class Keyboard(Channel):
    """Keyboard channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Keyboard channel; default is 'keyboard'
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Keyboard was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Event times in seconds
        - ['codes']: np.ndarray of str associated with keyboard events
    """

    def __init__(self, name: str, data_dict: parsed_keyboard) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                path_save_figures=data_dict.get("path_save_figures", None),
                trial_name=data_dict.get("trial_name", None),
                subject_id=data_dict.get("subject_id", None),
            ),
            data_dict.get("times", None),
        )
        self.codes = data_dict.get("codes", None)
        self.type = EnumChannelTypes.KEYBOARD

    def plot(self, save: Literal[True, False] = False) -> None:
        """Save Keyboard channel figure

        Parameters
        ----------
        save
            Set to `True` to save Keyboard figure to `path_save_figures`
        """

        plot.plot_channel(self, save=save)
        return self


class Waveform(Channel, sig_proc.SignalProcessing):
    """Waveform channel class

    Inherits from Channel and sig_proc.SignalProcessing

    Parameters
    ----------
    name
        Name of Waveform channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Waveform was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Waveform times in seconds
        - ['values']: np.ndarray - Waveform float values
        - ['units']: str - Measurement units (e.g. 'Volts')
        - ['sampling_frequency']: int - Sampling frequency of Wavemark
    """

    def __init__(self, name: str, data_dict: parsed_waveform) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                units=data_dict.get("units", None),
                sampling_frequency=data_dict.get("sampling_frequency", None),
                path_save_figures=data_dict.get("path_save_figures", None),
                trial_name=data_dict.get("trial_name", None),
                subject_id=data_dict.get("subject_id", None),
            ),
            data_dict.get("times", None),
        )
        self.values = data_dict.get("values", None)
        self.raw_values = self.values
        self.type = EnumChannelTypes.WAVEFORM

    def plot(self, save: Literal[True, False] = None) -> None:
        """Save Waveform channel figure

        Parameters
        ----------
        save
            Set to `True` to save Waveform figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self


class Wavemark(Channel):
    """Wavemark channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Wavemark channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Wavemark was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Wavemark times in seconds
        - ['values']: np.ndarray - Waveform float values
        - ['action_potentials']: list of lists - Each list is a Wavemark
        - ['units']: str - Measurement units (e.g. 'Volts')
        - ['sampling_frequency']: int - Sampling frequency of Wavemark
    """

    def __init__(self, name: str, data_dict: parsed_wavemark) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                units=data_dict.get("units", None),
                sampling_frequency=data_dict.get("sampling_frequency", None),
                path_save_figures=data_dict.get("path_save_figures", None),
                trial_name=data_dict.get("trial_name", None),
                subject_id=data_dict.get("subject_id", None),
            ),
            data_dict.get("times", None),
        )
        self.action_potentials = data_dict.get("action_potentials", None)
        self._calc_instantaneous_firing_frequency()
        self.type = EnumChannelTypes.WAVEMARK

    def _calc_instantaneous_firing_frequency(self):
        time1: float = self.times[0]
        inst_firing_frequency = list()
        for time2 in self.times[1:]:
            inst_firing_frequency.append(1 / (time2 - time1))
            time1 = time2
        self.inst_firing_frequency = np.array(inst_firing_frequency)

    def plot(self, save: Literal[True, False] = None):
        """Save Wavemark channel figure

        Parameters
        ----------
        save
            Set to `True` to save Wavemark figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self
