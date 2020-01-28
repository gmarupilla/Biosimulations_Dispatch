import pytest
from biosimulations_dispatch.utils import genAccessToken, parseTime
import datetime


def test_genAccessToken():
    string = genAccessToken()
    assert(len(string) == 16)


def test_parseTime():
    seconds = parseTime(time="2019-12-28T10:57:05")
    assert(seconds == datetime.datetime.utcfromtimestamp(1577530625))
