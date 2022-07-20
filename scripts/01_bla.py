from __future__ import annotations

from typing import NamedTuple

class aa(NamedTuple):
    df: str

class bb(aa):
    df2: str

if __name__ == '__main__':
    aa_ = aa(df='er')
    bb_ = bb(df2='er2')
    print(aa_)
    print(bb_)