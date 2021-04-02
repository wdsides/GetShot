import requests
import json
from opencage.geocoder import OpenCageGeocode 
from geopy.distance import geodesic
import schedule
import time
from datetime import date
from math import ceil
from twilio.rest import Client
from private_API_keys import twilio_sid, twilio_auth_token, phonenumber, twilionumber, geocoder_key

#Configuration
textNotifications=True #whether to receive SMS notifications
home = 'San Jose CA' #Your location
radiusMi = 60 #Search radius for CVS/Safeway; Walgreens ignores this value and always searches 25 miles
maxTexts = 3 #The program will run indefinitely until stopped or excepted, but to prevent spam, will only send this many text messages before SMS functionality is disabled
#End of configuration

if textNotifications:
    smsclient = Client(twilio_sid, twilio_auth_token)
geocoder = OpenCageGeocode(geocoder_key)
home = geocoder.geocode(home)
homeCoords=(home[0]['geometry']['lat'],home[0]['geometry']['lng'])
textLog=[]

def twilio_notify(body):
    if len(textLog)>maxTexts:
        print('Already sent %i texts, no more will be sent' %maxTexts)
        return
    textLog.append(smsclient.messages.create(to=phonenumber, from_=twilionumber, body=body))
    print('Sent text to %s' %(phonenumber))
    
def searchWalg(lat=home[0]['geometry']['lat'], long=home[0]['geometry']['lng'], state=home[0]['components']['state_code']):
    walg_cookies = {
        'XSRF-TOKEN': 'xgNRZBevh7/Vpg==.Bamtws483hxZpQ+ymiqC+y0Ng/NSfZV+Ke60+6SAMJg=',
        'session_id': 'eb3b9644-20a3-419b-840e-c0abf8359d88',
        'bm_sz': '3F020FB9F1A2D557B8D9735949FF08DC~YAAQTPo7F11wdHN4AQAA0ZnPjwspOAZn74hGYY3yUlX7gZU79w92N0bnzNyZJsMQmYr7WkVJvcJ1X2oO60VAIa48hsnyc6Dx3NLrEiQOgoG2Tc24osBsRP5e8LSr1ylGX4zF4OGbnYJzHOh0g/XyhYPqrBrltOA/qHMJbzNUhd2wwIKR2CULXxIOC22NiTBcOAQ=',
        'mt.sc': '%7B%22i%22%3A1617320451530%2C%22d%22%3A%5B%5D%7D',
        'mt.v': '2.1358662350.1617320451535',
        'at_check': 'true',
        's_ecid': 'MCMID%7C76463626635333007142587811141589522543',
        'AMCVS_5E16123F5245B2970A490D45%40AdobeOrg': '1',
        'mbox': 'session#dc2efc88a90a4008920120e90a323057#1617322312|PC#dc2efc88a90a4008920120e90a323057.34_0#1680565254',
        '_gcl_au': '1.1.1791247494.1617320453',
        's_cc': 'true',
        'AMCV_5E16123F5245B2970A490D45%40AdobeOrg': '-1124106680%7CMCIDTS%7C18719%7CMCMID%7C76463626635333007142587811141589522543%7CMCAID%7CNONE%7CMCOPTOUT-1617327653s%7CNONE%7CMCAAMLH-1617925253%7C7%7CMCAAMB-1617925253%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-18726%7CvVersion%7C5.2.0',
        'mt.mbsh': '%7B%22fs%22%3A1617320454207%7D',
        'rxVisitor': '1617320454406VPRPAGBPV367H8ORPODAEV0T3OV863N2',
        'bm_mi': '4DEC580FAA4B77739B6DC0861B5638FF~T8EbLeWiJn1kvx0pFZl+RDfnrs4hgQhpCG88kA2AGzDdeKN6Nhtx9yrXn0a7eo9t6xq5qDUZNwRg6IUdQXayQ/zNJwvsaiyj0FsN34dlyTirdtNUTotcbV7xRLLiuGmzgvdCsiwRHuDXznouTAHPzSXv3OIAPcdz/DYyJVTQqISa3nszu9dPMvMk0I+6uOCerLOQhqAAVTE801Ti+/i01bjrzwWbFJDqFjA0mZ2Ysa/WSrSFaQxLh2wlAMoUA4+dYjJceulkILsPS/NfMAcZwFdy367BvjyCSjn8JxFAL48xsTAG/iurhr260NOgyXU/',
        'wag_sid': 'u8lfocq6vzjq7gqrla9unzs7',
        'uts': '1617320463287',
        'ak_bmsc': 'F61F560B7D191563C45FB7E4A8BA702A173BFA4C2C2E0000025A666083B6AB3E~pl6zx3iJ8i4O9KPGF4NOiyauHTFpjmxg5JF2O064eRRwQ92A0VFrOnqGsMRIZ5lX+V+3cC9lQITzM4Q/qsOaCCDBIVw61RummqiuBDezGAoUvx3QUbmeAcKvmMWukJoV2mB3L/lCasiUKqbTvQSWhUQ0xHTY/v80aStl+Y6Bof0Q09m5i1HqJJR1rvqliFhqqX4vP+zGhEiGJ9nWJaE2qY5ay5jl9ZK/EMID2dgCNQgdk9xqYonbgcNzBvHq70OTiC',
        'fc_vnum': '1',
        'fc_vexp': 'true',
        'dtSa': '-',
        'USER_LOC': '5K48AZ9EjJsd1%2BhKAwBaTAuAIjJ7tdA3%2FnUIxy5wSvjTo6c5I8JPZfhLqcIjQ1HX',
        'gpv_Page': 'https%3A%2F%2Fwww.walgreens.com%2Ffindcare%2Fvaccination%2Fcovid-19%2Flocation-screening',
        'gRxAlDis': 'N',
        'rxvt': '1617322285467|1617320454412',
        '_abck': '4891F67D6739D24AEB164F19E9A9B464~0~YAAQTPo7F2twdHN4AQAALCXQjwVAtZ+nt2cbaKoAbSBeDeBoKKcHEramVXQJUNm7FWSd3acGnBveuVgIsJER2SLfjyFVJ9gt3CvMQ6p+0QoiB2uv8T+hIZM3rj0mLcwSDZnUXbhSl7D3TK3sneb9jebcqmmcNK7qszOA87zvpyCkG0xYiOtK9T7qGioS2lv8C/Q9LYeylkgT6CXYr6OFa7ZqN2Fd17SA7fh8bg3o7Bn+BwlfMHTuWIGn9Lkl1BlGSaiAxY6PhIZISQuxyjkDNdJigDRCfV2dZQHeQEUtW7zXgTFBpojKYMwZ0qmZY/fjkVaGsQwtZZOUsph0e0uLLRvdbMBicQCZIkM2or586ni0x5VAOdka4uC/2hcGRp2IsEzmXo0rFgP0glQv+88BZ7LR/FH4WonfLno7~-1~||-1||~-1',
        'dtLatC': '1',
        'akavpau_walgreens': '1617320789~id=990118b6a67c65a5cecb1d89438b7c2d',
        'bm_sv': '286440021695AE01FD01CDC4E54CF743~63x+T0EjbASjOvFoGUUBOobsa8/iIyOpN9V0nHlzLgXGzkGivVw1jYejbGdrFgn4nRXCpfQkWdG/PJUa8cNBoe7le6vbAWaRF+i8199KltadoLeUfiI7h0pYJqIeN0jh+KSEMSHL2hld/zPMhRbg1EjqQqBlBciHgwSIUS0o1e8=',
        's_sq': 'walgrns%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwg%25253Afindcare%25253Acovid19%252520vaccination%25253Alocation%25253Ascreening%2526link%253DSearch%2526region%253Dwag-body-main-container%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwg%25253Afindcare%25253Acovid19%252520vaccination%25253Alocation%25253Ascreening%2526pidt%253D1%2526oid%253DSearch%2526oidt%253D3%2526ot%253DSUBMIT',
    }
    walg_headers = {
        'authority': 'www.walgreens.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not\\"A\\\\Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'dnt': '1',
        'x-xsrf-token': 'ofCzLBxw/HBMZQ==.8dBDpIgVTt1bCFWpkwauCT2nMAyphdguAnQIyuv7IRE=',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.walgreens.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening',
        'accept-language': 'en-US,en;q=0.9',
    }
    print('Searching Walgreens...')
    curr_date = date.today().strftime('%Y-%m-%d')
    start_day = str(int(curr_date[9:10]) + 1)
    if len(start_day) < 2:
        start_day = "0" + start_day
    start_date = curr_date[0:8] + start_day
    walg_data = '{"position":{"latitude":' + str(lat) + ',"longitude":' + str(long) + '},"state":"' + state + '","vaccine":{"productId":""},"appointmentAvailability":{"startDateTime":"' + start_date + '"},"radius":25,"size":25,"serviceId":"99"}'
    try:
        r = requests.post('https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability', headers=walg_headers, cookies=walg_cookies, data=walg_data, timeout=10)
    except:
        return
    if r.status_code != 200:
        print('HTTP error - %i' %r.status_code)
        return
    payload = r.json()
    if payload['appointmentsAvailable']:
        body='Availability found at Walgreens in your area! https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
        print(body)
        if textNotifications:
            twilio_notify(body)
    else:
        print('nothing')

def searchSW():
    print('Searching Safeway...')
    mytime = ceil(time.time())
    try:
        r = requests.get("https://s3-us-west-2.amazonaws.com/mhc.cdn.content/vaccineAvailability.json?v={}".format(mytime), timeout=10)
    except:
        return
    if r.status_code != 200:
        print('HTTP error - %i' %r.status_code)
        return
    payload = r.json()
    nearbyAvail=[]
    for store in payload:
        if store['availability'] == 'yes' and geodesic(homeCoords, (store['lat'],store['long'])).miles < radiusMi:
            nearbyAvail.append(store)
    for i in nearbyAvail:
        body = 'Availability found at %s - https://www.mhealthappointments.com/covidappt' %i['address']
        print(body)
        if textNotifications:
            twilio_notify(body)
    if len(nearbyAvail) == 0:
        print('nope')


def searchCVS():
    try:
        with open('cityLUT.json') as json_file:
            cityLUT = json.load(json_file)
    except FileNotFoundError: 
        cityLUT = {}
    cvs_headers = {   
            "authority" : "www.cvs.com",
            "method": "GET",
            "path": "/immunizations/covid-19-vaccine.vaccine-status.CA.json?vaccineinfo",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "dnt": "1",
            "referer": "https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine",
            "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
             }
    cvs_url="https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.%s.json?vaccineinfo" %home[0]['components']['state_code']
    print('Searching CVS...')
    try:
        r = requests.get(cvs_url, headers=cvs_headers, timeout=10)
    except:
        return
    if r.status_code != 200:
        print('HTTP error - %i' %r.status_code)
        return
    results = json.loads(r.text)['responsePayloadData']['data']['CA']
    availableLocations=[]
    for row in results:
        if row['status'] == 'Available':
            availableLocations.append('%s %s' %(row['city'],row['state']))

    for city in availableLocations:
        if city not in cityLUT:
            citydata = geocoder.geocode(city)
            lat=citydata[0]['geometry']['lat']
            lng=citydata[0]['geometry']['lng']
            cityLUT[city]=(lat,lng)
            # print('Added %s' %city)
    with open('cityLUT.json', mode='w') as json_file:
        json.dump(cityLUT, json_file, indent=2)
    
    nearbyAvail=[]
    for city in availableLocations:
        distance = geodesic(homeCoords, cityLUT[city]).miles
        if distance < radiusMi:
            nearbyAvail.append(city)

    for i in nearbyAvail:
        body='Availability found at CVS in %s - https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine' %i
        print(body)
        if textNotifications:
            twilio_notify(body)
    if len(nearbyAvail) == 0:
        print('nada')

schedule.clear()
searchCVS()
searchSW()
searchWalg()
schedule.every(2).minutes.do(searchCVS)
schedule.every(2).minutes.do(searchWalg)
schedule.every(2).minutes.do(searchSW)
while True:
    schedule.run_pending()
    time.sleep(1)