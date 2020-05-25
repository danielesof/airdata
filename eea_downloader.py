import os
import json
import pycurl
import urllib
import io
import time
import csv
import requests
import pandas as pd
import certifi

def _HTTP_request(url, filename=None):
    '''metodo per la richiesta HTTP'''
    try:
        with open(f'{filename}.tmp', 'wb') if filename else io.BytesIO() as f:
            curl=pycurl.Curl()
            curl.setopt(pycurl.URL, url.encode('ascii', 'ignore'))
            curl.setopt(pycurl.WRITEDATA, f)
            curl.setopt(pycurl.FAILONERROR, True)
            
            curl.perform()
            curl.close()
            if filename:
                os.rename(f'{filename}.tmp', filename)
            else:
                return f.getvalue()
            
    except pycurl.error as err:
        print(err)
            

def search(country_code,city_name,pollutant,year_from,year_to,station,sampling_point,
           source,output,update_date,time_coverage):
    '''metodo per la creazione della query'''
    url= 'https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?'
    
    p_code={'As in PM10':5018,'BaP in PM10':5029,'C6H6':20,'Cd in PM10':5014,'CO':10,
            'Ni in PM10':5015, 'NO2':8,'NOX as NO2':9,'O3':7,'Pb in PM10':5012, 'PM10':5,
            'PM2.5':6001,'SO2':1}
    
    q = {'CountryCode': country_code, 'CityName': city_name, 'Pollutant': p_code[pollutant],
         'Year_from': year_from, 'Year_to': year_to, 'Station':station,
         'Samplingpoint':sampling_point, 'Source': source, 'Output':output, 'UpdateDate':update_date,
         'TimeCoverage':time_coverage}
    query=urllib.parse.urlencode(q, safe='():,\\[]',quote_via=urllib.parse.quote)
    q=url+query
    body=_HTTP_request(q,'linkDownloader')
    download_csv()
    return


def download_csv():
    '''metodo per il download nella local directory del file csv'''
    print('Download file: ')
    with open('linkDownloader', 'r') as f:
        for line in f:
            l=line.strip()
            l=l.lstrip('\ufeff')
            print(l)
            
            line=l.rsplit('/',1)
            name=line[-1]

            data=pd.read_csv(l)
            #print(data[0:3])
            _HTTP_request(l,name)
    f.close()


search('IT','Milano','As in PM10',2019,2020,'','', 'All','TEXT','','Year')
search('IT','Messina','PM10',2019,2020,'','', 'All','TEXT','','Year')
search('IT','Milano','SO2',2020,2020,'','', 'All','TEXT','','Last7days')
 