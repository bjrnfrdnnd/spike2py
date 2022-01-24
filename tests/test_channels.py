from pytest import approx

from spike2py import channels
from spike2py.channels import Channel
from spike2py.enums import EnumChannelTypes


def test_channels_event_init(channels_init, channels_mock):
    ECTs = EnumChannelTypes
    ch_type = ECTs.EVENT
    ch = channels.Event(**channels_init[ch_type])
    Ch = getattr(channels, ch_type.value.title())
    Ch: Channel
    assert ch.info.name == channels_mock[ch_type]["info"].name
    assert (ch.info.path_save_figures == channels_mock[ch_type]["info"].path_save_figures)
    assert ch.info.trial_name == channels_mock[ch_type]["info"].trial_name
    assert ch.info.subject_id == channels_mock[ch_type]["info"].subject_id
    assert list(ch.times) == list(channels_mock[ch_type]["times"])
    assert repr(ch) == Ch.get_repr(ch_type)


def test_channels_keyboard_init(channels_init, channels_mock):
    ECTs = EnumChannelTypes
    ch_type = ECTs.KEYBOARD
    ch = channels.Keyboard(**channels_init[ch_type])
    Ch = getattr(channels, ch_type.value.title())
    Ch: Channel
    assert ch.info.name == channels_mock[ch_type]["info"].name
    assert (ch.info.path_save_figures == channels_mock[ch_type]["info"].path_save_figures)
    assert ch.info.trial_name == channels_mock[ch_type]["info"].trial_name
    assert ch.info.subject_id == channels_mock[ch_type]["info"].subject_id
    assert list(ch.times) == list(channels_mock[ch_type]["times"])
    assert repr(ch) == Ch.get_repr(ch_type)


def test_channels_waveform_init(channels_init, channels_mock):
    ECTs = EnumChannelTypes
    ch_type = ECTs.WAVEFORM
    ch = channels.Waveform(**channels_init[ch_type])
    Ch = getattr(channels, ch_type.value.title())
    Ch: Channel
    assert "raw_values" in ch.__dir__()
    assert ch.info.name == channels_mock[ch_type]["info"].name
    assert (ch.info.path_save_figures == channels_mock[ch_type]["info"].path_save_figures)
    assert ch.info.trial_name == channels_mock[ch_type]["info"].trial_name
    assert ch.info.subject_id == channels_mock[ch_type]["info"].subject_id
    assert list(ch.times) == list(channels_mock[ch_type]["times"])
    assert ch.info.units == channels_mock[ch_type]["info"].units
    assert list(ch.values) == list(channels_mock[ch_type]["values"])
    assert (ch.info.sampling_frequency == channels_mock[ch_type]["info"].sampling_frequency)
    assert repr(ch) == Ch.get_repr(ch_type)


def test_channels_wavemark_init(channels_init, channels_mock):
    ECTs = EnumChannelTypes
    ch_type = ECTs.WAVEMARK
    ch = channels.Wavemark(**channels_init[ch_type])
    Ch = getattr(channels, ch_type.value.title())
    Ch: Channel
    assert ch.info.name == channels_mock[ch_type]["info"].name
    assert (ch.info.path_save_figures == channels_mock[ch_type]["info"].path_save_figures)
    assert ch.info.trial_name == channels_mock[ch_type]["info"].trial_name
    assert ch.info.subject_id == channels_mock[ch_type]["info"].subject_id
    assert list(ch.times) == list(channels_mock[ch_type]["times"])
    assert ch.info.units == channels_mock[ch_type]["info"].units
    assert (ch.info.sampling_frequency == channels_mock[ch_type]["info"].sampling_frequency)
    assert (ch.action_potentials == channels_mock[ch_type]['action_potentials'])
    assert (ch.inst_firing_frequency == approx(channels_mock[ch_type]['instantaneous_firing_frequency']))
    assert repr(ch) == Ch.get_repr(ch_type)
