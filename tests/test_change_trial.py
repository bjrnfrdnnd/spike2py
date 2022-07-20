import copy

from spike2py import trial
from spike2py.channels import Channel
from spike2py.enums import EnumChannelTypes
from spike2py.trial import TrialInfo, load


def test_bla(trial_default):
    print()
    info = TrialInfo(file=trial_default)
    actual = trial.Trial(info)
    print(f'loading {actual.info.file.name}: {actual.get_short_channel_info()}: {actual.get_short_channel_info()}')
    print()

    fp0 = actual.get_safe_path_pickle()
    fp1 = fp0.parent / f'{fp0.stem}_1{fp0.suffix}'
    fp = fp1
    actual.save(file=fp)


    ch1 = None
    for v in actual.channel_dict.values():
        v: Channel
        if v.type == EnumChannelTypes.WAVEFORM.value:
            ch1 = v


    actual = load(file=fp)
    fp2 = fp0.parent / f'{fp0.stem}_2{fp0.suffix}'
    fp = fp2
    print(fp)
    actual.remove(id_='triangle')
    print(f'writing {fp.name} {actual.info.file.name}: {actual.get_short_channel_info()}')
    actual.save(file=fp)
    actual = load(file=fp)
    print(f'loading {fp.name} {actual.info.file.name}: {actual.get_short_channel_info()}')
    print()

    actual = load(file=fp2)
    fp3 = fp0.parent / f'{fp0.stem}_3{fp0.suffix}'
    fp = fp3
    print(fp)
    actual.add(name=ch1.name, ch=ch1)
    ch2 = copy.deepcopy(ch1)
    ch2.name = 'df'
    actual.add(name=ch2.name, ch=ch2)
    print(f'writing {fp.name} {actual.info.file.name}: {actual.get_short_channel_info()}')
    actual.save(file=fp)
    actual = load(file=fp)
    print(f'loading {fp.name} {actual.info.file.name}: {actual.get_short_channel_info()}')
    print()

    files = list(fp0.parent.glob('*'))
    files = sorted(files)
    for f in files:
        stat = f.stat()
        print(f'{f.name} {stat.st_size}')

