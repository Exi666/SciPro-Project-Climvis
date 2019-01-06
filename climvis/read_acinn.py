# -*- coding: utf-8 -*-
"""
    Author:         Birgit Bacher
    Purpose:        Read data from ACINN
    Date:           Tue Dec  4 08:55:50 2018
    Arguments:      time (1,3,7)
                    station(innsbruck, ellboegen, sattelberg, obergurgl)
    Outputs:
    Dependencies:

"""

import json
import urllib
import urllib.request
from datetime import datetime
import pytz
import numpy as np


class AcinnData():
    """ Read data from ACINN page"""

    def __init__(self, timespan, station):
        """
        Initialize object:
        Input:
            timespan: (1,3,7 days)
            station:  (innsbruck, ellboegen, sattelberg, obergurgl)
        """
        self.timespan = timespan
        self.station = station

    def get_data(self):
        """Read raw data"""
        timestr = str(self.timespan)
        url = 'http://acinn.uibk.ac.at/' + self.station + '/' + timestr
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            raise Exception('could not read from URL')
        except urllib.error.URLError:
            raise Exception('could not read from URL')
        self.raw_data = json.loads(response.read().decode())
        self.keys = []

    def conv_raw(self):
        """ make data better accessible (.param) """
        try:
            for key in self.raw_data.keys():
                setattr(self, key, self.raw_data[key])
                self.keys.append(key)
        except AttributeError:
            raise Exception('you might have called get_data method first')

    def conv_date(self):
        """ date & time conversions """
        try:
            self.datumsec = [x / 1000 for x in self.datumsec]
        except AttributeError:
            raise Exception('you might have called get_data method first')
        self.timeutc = [datetime.utcfromtimestamp(x) for x in self.datumsec]
        tz = pytz.timezone('Europe/Vienna')
        self.time = [datetime.fromtimestamp(x, tz) for x in self.datumsec]
        self.keys.append('time')

    def conv_units(self):
        """ convert units & keys
        pass if parameter not measured at this station"""
        try:
            self.kmwind = [x * 3.6 for x in self.ff]
            self.keys.append('kmwind')
        except AttributeError:
            pass
        try:
            self.rm = [x / 6 for x in self.rr]
            self.crm = np.cumsum(self.rm)
            self.keys.append('rm')
        except AttributeError:
            pass
        try:
            self.sop = [x * 10 for x in self.so]
            self.keys.append('sop')
        except AttributeError:
            pass

    def make_dict(self):
        """Dictionary with meaningful names and units"""
        self.dict = {}
        if 'rr' in self.keys:
            self.dict['rr'] = 'Precipitationrate [mm/h]'
        if 'dd' in self.keys:
            self.dict['dd'] = 'Winddirection [°]'
        if 'tp' in self.keys:
            self.dict['tp'] = 'Dewpoint [°C]'
        if 'p' in self.keys:
            self.dict['p'] = 'Pressure [hPa]'
        if 'tl' in self.keys:
            self.dict['tl'] = 'Temperature [°C]'
        if 'so' in self.keys:
            self.dict['so'] = 'Sunshine duration [min/10min]'
        if 'ff' in self.keys:
            self.dict['ff'] = 'Windspeed [m/s]'
        if 'datumsec' in self.keys:
            self.dict['datumsec'] = 'Timestamp [seconds since 1970]'
        if 'time' in self.keys:
            self.dict['time'] = 'Timestamp'
        if 'kmwind' in self.keys:
            self.dict['kmwind'] = 'Windspeed [km/h]'
        if 'rm' in self.keys:
            self.dict['crm'] = 'Cumulated precipitation [mm]'
        if 'sop' in self.keys:
            self.dict['sop'] = 'Sunshine duration [%]'
        if 'rf' in self.keys:
            self.dict['rf'] = 'Relative humidity [%]'
