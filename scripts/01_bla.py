from __future__ import annotations

from typing import NamedTuple


class Aa(NamedTuple):
    df: str


if __name__ == '__main__':
    aa_ = Aa(df='er')
    print(aa_)
