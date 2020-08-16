from collections import namedtuple

import numpy as np

from spike2py import plot, sig_proc


ChannelDetails = namedtuple(
    "Details", "name units sampling_frequency path_save_figures trial_name subject_id",
)
ChannelDetails.__new__.__defaults__ = (None, None, None, None, None, None)


class Channel:
    """Base class for all channel types

   Parameters
    ----------
    details: namedtuple
        details.name: str, default None
            Name of channel (.e.g 'left biceps')
        details.units: str, default None
            Units of recorded signal (e.g., 'Volts' or 'Nm')
        details.sampling_frequency: int, default None
            In Hertz (e.g. 2048)
        details.path: pathlib.Path
            Defaults to path where data initially retrieved
        details.trialname: str
            Defaults to name of data file
        details.subject_id: str
    times: numpy.ndarray
        Sample times of data or events, in seconds
    """

    def __init__(self, details, times):
        self.details = details
        self.times = times


class Event(Channel):
    """Event channel class
    Parameters
    ----------
    name: str
        Channel name
    data_dict: dict
        data_dict['times']: np.array of event times in seconds
    """

    def __init__(self, name, data_dict):
        super().__init__(
            ChannelDetails(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self):
        return "Event channel"

    def plot(self, save=None):
        plot.channel(self, save=save)


class Keyboard(Channel):
    """Keyboard channel class

    Parameters
    ----------
    name: str
        Channel name
    data_dict: dict
        data_dict['times']: np.array of times of keyboard events, in seconds
        data_dict['codes']: np.array of str associated with keyboard events
    """

    def __init__(self, name, data_dict):
        self.codes = data_dict["codes"]
        super().__init__(
            ChannelDetails(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self):
        return "Keyboard channel"

    def plot(self, save=None):
        plot.channel(self, save)


class Waveform(Channel, sig_proc.SignalProcessing):
    """Waveform channel class

        Parameters
        ----------
    data_dict: dict
        data_dict['times']: np.array of times of recorded signal, in seconds
        data_dict['values']: np.array of recorded signal values
        data_dict['units']: str describing measurement units (e.g. 'Volts')
        data_dict['sampling_frequency']: int
    """

    def __init__(self, name, data_dict):
        details = ChannelDetails(
            name=name,
            units=data_dict["units"],
            sampling_frequency=data_dict["sampling_frequency"],
            path_save_figures=data_dict["path_save_figures"],
            trial_name=data_dict["trial_name"],
            subject_id=data_dict["subject_id"],
        )
        self.values = data_dict["values"]
        self.raw_values = self.values
        super().__init__(details, data_dict["times"])

    def __repr__(self):
        return "Waveform channel"

    def plot(self, save=None):
        plot.channel(self, save)


class Wavemark(Channel):
    """Wavemark channel class

    Parameters
    ----------
    data_dict: dict
        data_dict['times']: np.array of action potential times, in seconds
        data_dict['action_potentials']: list of lists, where each list is a
            wavemark.
        data_dict['units']: str describing measurement units (e.g. 'Volts')
        data_dict['sampling_frequency']: int
    """

    def __init__(self, name, data_dict):
        details = ChannelDetails(
            name=name,
            units=data_dict["units"],
            sampling_frequency=data_dict["sampling_frequency"],
            path_save_figures=data_dict["path_save_figures"],
            trial_name=data_dict["trial_name"],
            subject_id=data_dict["subject_id"],
        )
        super().__init__(details, data_dict["times"])
        self.action_potentials = data_dict["action_potentials"]
        self._calc_instantaneous_firing_frequency()

    def __repr__(self):
        return "Wavemark channel"

    def _calc_instantaneous_firing_frequency(self):
        time1 = self.times[0]
        inst_firing_frequency = list()
        for time2 in self.times[1:]:
            inst_firing_frequency.append(1 / (time2 - time1))
        self.inst_firing_frequency = np.array(inst_firing_frequency)

    def plot(self, save=None):
        plot.channel(self, save)
