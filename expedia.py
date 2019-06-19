import requests
import requests
import re
from lxml import html
import json
import time
from datetime import datetime
from datetime import timedelta

strInputHotel = "Park Plaza London Riverbank"
strcity= "London"
strCheckin = "23/07/2019"
strAdult = "2"
Strnights = 1

http_proxy = "http://sachin:sachin@123@barcelona.wonderproxy.com:11000"
https_proxy = "https://sachin:sachin@123@barcelona.wonderproxy.com:11000"
proxies = {'http': http_proxy,
           'https': https_proxy}



headers_get = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'Host': 'www.expedia.co.uk',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

home_url="https://www.expedia.co.uk/"
response=requests.get(home_url,proxies=proxies,headers=headers_get)
homepage= response.text
with open("homepage.html", 'w', encoding='utf-8') as file:
    file.write(homepage)

startsiteid = homepage.find(',"siteId":')+ len(',"siteId":')
endsiteid = homepage.find(',',startsiteid)
strsiteid = homepage[startsiteid:endsiteid]

startguid = homepage.find(',"guid"')+ len(',"guid"')
endguid = homepage.find('",',startguid)
strguid = homepage[startguid:endguid]

################hotel input###############
strInputHotel_1 = strInputHotel.replace(" ","%20")
hotelapi_url="https://www.expedia.co.uk/api/v4/typeahead/"
hotelapi_url = hotelapi_url + strInputHotel_1 + "?callback=cb_1559898081535_626187901&client=Homepage&siteid="+ strsiteid + "&guid="
hotelapi_url = hotelapi_url + strguid + "&lob=HOTELS&locale=en_GB&expuserid=-1&regiontype=2047&ab=&dest=true&maxresults=8"
hotelapi_url = hotelapi_url + "&features=contextual_ta%7Cpostal_code%7Cuta_client%7Cgoogle%7Cmultiregion_parent%7Cta_hierarchy&format=jsonp&device=Desktop&browser=Chrome&personalize=true"

headers_get['accept'] = 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
headers_get['X-Requested-With'] = 'XMLHttpRequest'


response=requests.get(hotelapi_url,proxies=proxies,headers=headers_get)
hotelapiresp = response.text.replace('cb_1559898081535_626187901(','').replace(')','')
with open("hotelapiresp.html", 'w', encoding='utf-8') as file:
    file.write(hotelapiresp)

# date_1 = datetime.strptime(strCheckin, "%m/%d/%y")

# end_date = date_1 + datetime.timedelta(days=10)

hotelresp = json.loads(hotelapiresp)
strlat = hotelresp['sr'][0]['coordinates']['lat']
strlong = hotelresp['sr'][0]['coordinates']['long']
strhotelId = hotelresp['sr'][0]['hotelId']
strcityId = hotelresp['sr'][0]['cityId']


hotel_listurl = "https://www.expedia.co.uk/Hotel-Search-Data?responsive=true&selected="
hotel_listurl = hotel_listurl + strhotelId + "&latLong=" + strlat +"%2C" + strlong + "&regionId="
hotel_listurl = hotel_listurl + strcityId + "&destination=" + strcity + "&startDate=25%2F06%2F2019&endDate=26%2F06%2F2019&rooms=1&adults=2&searchPriorityOverride=213&timezoneOffset=19800000&langid=2057&hsrIdentifier=HSR&?1559604158081"

headers_get['accept'] = '*/*'

hotel_listresp = requests.post(hotel_listurl, proxies=proxies, headers=headers_get)
print(hotel_listresp.status_code)
with open("hotel_listresp.html", 'w', encoding='utf-8') as file:
    file.write(hotel_listresp.text)

list_response = hotel_listresp.json()

hotel_url1 = list_response['searchResults']['retailHotelModels'][0]['infositeUrl']
hotel_url2 = list_response['searchResults']['infositeQueryString']

# hotel_url = hotel_url1 + hotel_url2
hotel_url = 'https://www.expedia.co.uk/London-Hotels-Park-Plaza-London-Riverbank.h1183908.Hotel-Information?&chkin=25/06/2019&chkout=26/06/2019&rm1=a2&exp_dp=345.6&exp_ts=1560236126477&exp_curr=GBP&swpToggleOn=false&exp_pg=HSR'

headers_get['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers_get['upgrade-insecure-requests'] = '1'

hotelpageresp = requests.get(hotel_url, proxies=proxies, headers=headers_get)
with open("hotel_pageresp.html", 'w', encoding='utf-8') as file:
    file.write(hotelpageresp.text)

try:
    test1 = html.fromstring(hotelpageresp.text).xpath('//*[contains(text(), "infosite.token")]/text()')
    test2 = html.fromstring(hotelpageresp.text).xpath('//*[contains(text(), "infosite.partnerTimestamp")]/text()')
    test3 = html.fromstring(hotelpageresp.text).xpath('//*[contains(text(), "infosite.partnerPrice")]/text()')
    # test4 = html.fromstring(hotelpageresp.text).xpath('//*[contains(text(), "infosite.tla")]/text()')
except:
    test1 = ''
    test2 = ''
    test3 = ''
    # test4 = ''

search_index = test1[0].find("infosite.token = '")
start_index = test1[0].find("infosite.token = '", search_index)
end_index = test1[0].find("';",start_index)

token = test1[0][start_index + len("infosite.token = '"):end_index]

# ====================================================================================
search_index1 = test2[0].find("infosite.partnerTimestamp = '")
start_index1 = test2[0].find("infosite.partnerTimestamp = '", search_index1)
end_index1 = test2[0].find("';",start_index1)

partnerts = test2[0][start_index1 + len("infosite.partnerTimestamp = '"):end_index1]

# ====================================================================================
search_index2 = test3[0].find("infosite.partnerPrice = '")
start_index2 = test3[0].find("infosite.partnerPrice = '", search_index2)
end_index2 = test3[0].find("';",start_index2)

partnerprice = test3[0][start_index2 + len("infosite.partnerPrice = '"):end_index2]

# # ====================================================================================
# search_index3 = test4[0].find('infosite.tla = "')
# start_index3 = test4[0].find('infosite.tla = "', search_index3)
# end_index3 = test4[0].find("';",start_index3)
#
# tla = test4[0][start_index3 + len('infosite.tla = "'):end_index3]

# ====================================================================================
# search_index2 = test2[0].find('hwrqCacheKey')
# start_index2 = test2[0].find('CacheKey', search_index2)
# end_index2 = test2[0].find('\\', start_index2)
#
# cachekey = test2[0][start_index2+len('hwrqCacheKey":"'):end_index2]

try:
    test = html.fromstring(hotelpageresp).xpath('//*[contains(text(), "infosite.offersData")]/text()')
except:
    test = ''

if hotelpageresp != test:

    ts = int(round(time.time() * 1000))
    print(ts)

    retry_url = 'https://www.expedia.co.uk/infosite-api/1183908/getOffers?clientid=KLOUD-HIWPROXY&token=' + str(token)
    retry_url = retry_url + '&brandId=236'
    retry_url = retry_url + '&countryId=190'
    retry_url = retry_url + '&isVip=false&chid=&partnerName=HSR&partnerPrice=' + str(partnerprice)
    retry_url = retry_url + '&partnerCurrency=GBP'
    retry_url = retry_url + '&partnerTimestamp=' + str(partnerts)
    retry_url = retry_url + '&adults=2&children=0&=undefined'
    retry_url = retry_url + '&chkin=25%2F6%2F2019&chkout=26%2F6%2F2019'
    retry_url = retry_url + '&exp_dp=0&exp_ts=' + str(partnerts)
    retry_url = retry_url + '&exp_curr=GBP&swpToggleOn=false&exp_pg=HSR&daysInFuture=&stayLength='
    retry_url = retry_url + '&ts=' + str(ts)
    retry_url = retry_url + '&evalMODExp=true&tla=LON'

    headers_get['accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers_get['referer'] = hotel_url
    headers_get['x-requested-with'] = 'XMLHttpRequest'

    offerspageresp = requests.get(retry_url, proxies=proxies, headers=headers_get)
    print(offerspageresp.status_code)
    with open("offers_pageresp.html", 'w', encoding='utf-8') as file:
        file.write(offerspageresp.text)