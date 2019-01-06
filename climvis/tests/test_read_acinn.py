# -*- coding: utf-8 -*-

from climvis.read_acinn import AcinnData
import pytest


def test_generate_obj():

    data = AcinnData(7, 'innsbruck')
    assert isinstance(data, AcinnData)
    assert data.station == 'innsbruck'


def test_get_data():

    data = AcinnData(7, 'innsbruck')
    data.get_data()
    assert isinstance(data.raw_data, dict)

    data = AcinnData(7, 'muenchen')
    with pytest.raises(Exception) as excinfo:
        data.get_data()
    assert 'could not read from URL' in str(excinfo.value)


def test_conv_raw():

    data = AcinnData(7, 'innsbruck')
    data.get_data()
    data.conv_raw()
    assert isinstance(data.keys, list)

    data = AcinnData(7, 'innsbruck')
    with pytest.raises(Exception) as excinfo:
        data.conv_raw()
    assert 'you might have called get_data method first' in str(excinfo.value)


def test_conv_date():

    data = AcinnData(7, 'innsbruck')
    data.get_data()
    data.conv_raw()
    data.conv_date()
    assert isinstance(data.timeutc, list)

    data = AcinnData(7, 'innsbruck')
    with pytest.raises(Exception) as excinfo:
        data.conv_date()
    assert 'you might have called get_data method first' in str(excinfo.value)
