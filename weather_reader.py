#!/usr/bin/python

# -*- coding: utf-8 -*-
from urllib import urlencode
import urllib2
import urllib
from lxml import etree
from lxml import objectify
import string
import re
import os

FREE_API_KEY = ""
PREMIUM_API_KEY = ""

_keytype = "free"
_key = FREE_API_KEY
_myIP = ""
_location = ""

_filepath="/tmp/images/"

def myIP():
    idx1 = idx2 = 0
    myip=""
    global _myIP

    try:
        dyndns = urllib2.urlopen("http://checkip.dyndns.com/")
        myip = dyndns.read()

        idx1 = string.find( myip, "Address: ", idx1)
        idx1 = idx1 + "Address: ".__len__()
        idx2 = string.find( myip, "</body>", idx1)
        _myIP = myip[idx1:idx2]

        return True
    except urllib2.URLError:
        return False


def internet_on():
    """fast test by trying one of google IPs"""
    try:
        #unfortunately sometimes google is unstable in China
        urllib2.urlopen('http://www.baidu.com',timeout=3)
        return True
    except urllib2.URLError:
        try:
            urllib2.urlopen('http://www.google.com',timeout=3)
            return True
        except urllib2.URLError:
            return False

def setKeyType(keytype="free"):
    """ keytype either "free" or "premium", set the key if it exists"""
    global _key, _keytype, FREE_API_KEY, PREMIUM_API_KEY

    keytype = keytype.lower()
    if keytype in ("f", "fr", "free"):
        _keytype = "free"
        if FREE_API_KEY == "":
            print "Please set FREE_API_KEY"
            return False
        else:
            _key = FREE_API_KEY
            return True
    elif keytype.startswith("prem") or keytype in ("nonfree", "non-free"):
        _keytype = "premium"
        if PREMIUM_API_KEY == "":
            print "Please set PREMIUM_API_KEY"
            return False
        else:
            _key = PREMIUM_API_KEY
            return True
    else:
        print "invalid keytype", keytype
        return False

def setKey(key, keytype):
    """ if keytype is valid, save a copy of key accordingly
        and check if the key is valid """
    global _key, _keytype, FREE_API_KEY, PREMIUM_API_KEY

    keytype = keytype.lower()
    if keytype in ("f", "fr", "free"):
        keytype = "free"
        FREE_API_KEY = key
    elif keytype.startswith("prem") or keytype in ("nonfree", "non-free"):
        keytype = "premium"
        PREMIUM_API_KEY = key
    else:
        print "invalid keytype", keytype
        return

    oldkey = _key
    oldkeytype = _keytype
    _key = key
    _keytype = keytype

    w = LocalWeather("london")
    # w.data != False rather than w.data to suppress Python 2.7 FurtureWarning:
    # "The behavior of this method will change in future versions...."
    if w is not None and hasattr(w, 'data') and w.data != False:
        return True
    else:
        print "The key is not valid."
        _key = oldkey
        _keytype = oldkeytype
        return False

class WWOAPI(object):
    """ The generic API interface """
    def __init__(self, q, **keywords):
        """ query keyword is always required for all APIs """
        if _key == "":
            print "Please set key using setKey(key, keytype)"
        else:
            if internet_on():
                self.setApiEndPoint(_keytype == "free")
                self._callAPI(q=q, key=_key, **keywords)
            else:
                print "Internet connection not available."

    def setApiEndPoint(self, freeAPI):
        if freeAPI:
            self.apiEndPoint = self.FREE_API_ENDPOINT
        else:
            self.apiEndPoint = self.PREMIUM_API_ENDPOINT

    def _callAPI(self, **keywords):
        for arg in keywords:
            if keywords[arg] != None:
                if keywords[arg] in ("No", "NO", "None"):
                    keywords[arg] = "no"
                elif keywords[arg] in ("Yes", "YES", "Yeah"):
                    keywords[arg] = "yes"
            else:
                del keywords[arg]

        url = self.apiEndPoint + "?" + urlencode(keywords)
        try:
            response = urllib2.urlopen(url).read()
        except urllib2.URLError:
            print "something wrong with the API server"
            return

        # if the key is invalid it redirects to another web page
        if response.startswith("<?xml "):
            self.data = objectify.fromstring(response)
            if self.data is not None and hasattr(self.data, 'error') and self.data.error != False:
                print self.data.error.msg
                self.data = False
        else:
            self.data = False

class LocalWeather(WWOAPI):
    FREE_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/weather.ashx"
    PREMIUM_API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/premium-weather-V2.ashx"

    def __init__(self, q, num_of_days=1, **keywords):
        """ q and num_of_days are required. max 7 days for free and 15 days for premium """
        super(LocalWeather, self).__init__(
            q, num_of_days=num_of_days, **keywords)

class LocationSearch(WWOAPI):
    FREE_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/search.ashx"
    PREMIUM_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/search.ashx"

class MarineWeather(WWOAPI):
    FREE_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/marine.ashx"
    PREMIUM_API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/marine.ashx"

class PastWeather(WWOAPI):
    FREE_API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
    PREMIUM_API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"

    def __init__(self, q, date=None, **keywords):
        """ q and date are required for free API. sometimes date is optional for premium API """
        super(PastWeather, self).__init__(
            q, date=date, **keywords)

class TimeZone(WWOAPI):
    FREE_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/tz.ashx"
    PREMIUM_API_ENDPOINT = "http://api.worldweatheronline.com/free/v1/tz.ashx"

if __name__ == "__main__":

    if internet_on() :
        if myIP():
           _location = _myIP
        else:
           _location = "Rome"
        #
        if setKey("YOUR_KEY_PLEASE", "free"):
            # weather = LocalWeather("8.8.8.8")
            print "Location: "+_location
            weather = LocalWeather(_location)
            # Scrivo il file con le info del meteo corrente
            weather_condition = '{\"tempo_attuale\":\"'+weather.data.current_condition.weatherDesc + '\",'
            weather_condition = weather_condition + '\"temperatura\":\"' + str(weather.data.current_condition.temp_C) + 'C\",'
            weather_condition = weather_condition + '\"umidita\":\"' + str(weather.data.current_condition.humidity) + '%\",'
            weather_condition = weather_condition + '\"pressione\":\"' + str(weather.data.current_condition.pressure) + 'hP\",'
            weather_condition = weather_condition + '\"pioggia\":\"' + str(weather.data.current_condition.precipMM) + 'mm\",'
            weather_condition = weather_condition + '\"icona\":\"' + _filepath+'curr_weather.png\"}'
            output = open(_filepath+"curr_weather.txt","wb+")
            output.write( weather_condition)
            output.close()
            # Scarico l'icona del meteo corrente
            URLweather = weather.data.current_condition.weatherIconUrl
            os.system("wget -q -O "+_filepath+"curr_weather.png "+URLweather)

            #print
            #print objectify.dump(weather.data.current_condition)

            #print
            weather = LocalWeather(_location, num_of_days=3)

            #
            today = weather.data.weather[0]
            tomorrow = weather.data.weather[1]
            twodayslater = weather.data.weather[2]
            #
            weather_condition = '{\"giorno\":"' + today.date + '\",'
            weather_condition = weather_condition + '\"tempo\":\"'   + today.weatherDesc + '\",'
            weather_condition = weather_condition + '\"tMax\":\"'    + str(today.tempMaxC) + 'C\",'
            weather_condition = weather_condition + '\"tMin\":\"'    + str(today.tempMinC) + 'C\",'
            weather_condition = weather_condition + '\"pioggia\":\"' + str(today.precipMM) + 'mm\",'
            weather_condition = weather_condition + '\"icona\":\"' + _filepath+'today_weather.png\"}'
            #weather_condition = re.sub("[^_a-zA-Z0-9 :?!@#=+-]", '', weather_condition)
            output = open(_filepath+"today_weather.txt","wb+")
            output.write( weather_condition)
            output.close()
            # Scarico l'icona del meteo di oggi
            URLweather = today.weatherIconUrl
            os.system("wget -q -O "+_filepath+"today_weather.png "+URLweather)
            #
            weather_condition = '{\"giorno\":"' + tomorrow.date + '\",'
            weather_condition = weather_condition + '\"tempo\":\"'    + tomorrow.weatherDesc + '\",'
            weather_condition = weather_condition + '\"tMax\":\"'     + str(tomorrow.tempMaxC) + 'C\",'
            weather_condition = weather_condition + '\"tMin\":\"'     + str(tomorrow.tempMinC) + 'C\",'
            weather_condition = weather_condition + '\"pioggia\":\"'  + str(tomorrow.precipMM) + 'mm\",'
            weather_condition = weather_condition + '\"icona\":\"' + _filepath+'tomorrow_weather.png\"}'
            #weather_condition = re.sub("[^_a-zA-Z0-9 :?!@#=+-]", '', weather_condition)
            output = open(_filepath+"tomorrow_weather.txt","wb+")
            output.write( weather_condition)
            output.close()
            # Scarico l'icona del meteo di domani
            URLweather = tomorrow.weatherIconUrl
            os.system("wget -q -O "+_filepath+"tomorrow_weather.png "+URLweather)
            #
            weather_condition = '{\"giorno\":"' + twodayslater.date + '\",'
            weather_condition = weather_condition + '\"tempo\":\"'     + twodayslater.weatherDesc + '\",'
            weather_condition = weather_condition + '\"tMax\":\"'      + str(twodayslater.tempMaxC)  + 'C\",'
            weather_condition = weather_condition + '\"tMin\":\"'      + str(twodayslater.tempMinC) + 'C\",'
            weather_condition = weather_condition + '\"pioggia\":\"'   + str(twodayslater.precipMM) + 'mm\",'
            weather_condition = weather_condition + '\"icona\":\"' + _filepath+'twodayslater_weather.png\"}'
            #weather_condition = re.sub("[^_a-zA-Z0-9 :?!@#=+-]", '', weather_condition)
            output = open(_filepath+"twodayslater_weather.txt","wb+")
            output.write( weather_condition)
            output.close()
            # Scarico l'icona del meteo dopodomani
            URLweather = twodayslater.weatherIconUrl
            os.system("wget -q -O "+_filepath+"twodayslater_weather.png "+URLweather)
            
            os.system("convert "+_filepath+"today_weather.png -resize 32x32 "+_filepath+"today_weather.rgb")
            os.system("convert "+_filepath+"tomorrow_weather.png -resize 32x32 "+_filepath+"tomorrow_weather.rgb")
            os.system("convert "+_filepath+"twodayslater_weather.png -resize 32x32 "+_filepath+"twodayslater_weather.rgb")

            #print
            #print objectify.dump(tomorrow)

            #print



