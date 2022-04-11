from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Token:
    id: int
    login: str
    access_token: str
    refresh_token: str

    @classmethod
    def from_dict(cls, adict: dict) -> Token:
        return Token(
            id=adict['id'],
            login=adict['login'],
            access_token=adict['access_token'],
            refresh_token=adict['refresh_token']
        )

    def to_dict(self) -> dict:
        return self.__dict__
