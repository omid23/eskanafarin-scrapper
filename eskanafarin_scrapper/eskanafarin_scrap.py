import sys
import traceback

import requests
from bs4 import BeautifulSoup
from functions import login_session_abs24
from functions import deactivate_abs24_session
from string import digits


def get_eskan_afarinan(user_name, password, scrapping_pages=10):
    try:
        page_number = 1
        authentication = login_session_abs24(user_name, password)
        while page_number <= scrapping_pages:
            url = "https://abs24.ir/AdminsforAbs/cls_estate.php"
            '''
             to get different trading types, change the type parameter
             type: 1 -> rent
             type:2 -> sell
             '''
            payload = f"Action=Showesearch&wherestr=&page={page_number}"

            headers = {
                'Connection': 'keep-alive',
                'Accept': 'text/html, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap '
                              'Chromium/81.0.4044.129 Chrome/81.0.4044.129 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://abs24.ir',
                'Referer': 'http://abs24.ir/profile.php',
                'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
                'Cookie': 'PHPSESSID=' + authentication,

            }

            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.content, "lxml")

            mcontent = soup.find('body')
            hrefs = mcontent.find_all('a')
            items = soup.find_all('div', class_='col-md-12 col-sm-12 col-xs-12')

            for item in range(len(items)):
                mortgage_fee = None
                rent_fee = None
                price_fee = None
                additional_data = dict()
                href = hrefs[item]['href']
                token = href.split("?")[1].split("&")[0].split("bcode=")[1]

                url_detail = f"https://abs24.ir/maindetails.php?bcode={str(token)}"
                url = url_detail

                payload2 = "Action=Showesearch&wherestr=&type=1&btype=1&minmeter=0&maxmeter=0&minrent=0&maxrent=0" \
                           "&minrahn=0&maxrahn=0&minprice=0&maxprice=0&address=&bid=0&sub=&first=0&mintotal=0" \
                           "&maxtotal=0&firstname=&date1=&date2=&old=0&home=0&secondstreet=&mid=0&show=0&area= "

                response_detail = requests.request("POST", url_detail, headers=headers, data=payload2)
                soup_detail = BeautifulSoup(response_detail.content, 'lxml')
                item_detail = soup_detail.find('div', class_='Item')

                # Getting title
                title = item_detail.find('p').text
                title = title
                # Getting address
                remove_digits = str.maketrans('', '', digits)
                address_element = item_detail.find('p').text

                # Getting meter
                meter_element = item_detail.find('span').text.replace("متری", '').replace(' ', '')

                meter = int(meter_element)

                elements = soup_detail.find('div', class_="ConfigMelk").find_all('li')

                for element in elements:

                    key = element.text
                    if key is not None:
                        value = element.find('span').text
                        key = key.replace(':', '').strip().replace('مشترک', '').replace('مستقل', '')
                        split_key = key.split(' ')
                        specific_keys = ' '.join(split_key[0:2])
                        specific_keys = specific_keys.translate(remove_digits).replace('/', '')
                        additional_data[specific_keys] = value
                item_element = item_detail.find_all('h2')
                trading_type_element = item_element[1].text

                for trade_type in item_element[1]:
                    if "رهن واجاره" in trade_type:
                        trading_type_element = "رهن واجاره"
                    elif "رهن کامل" in trade_type:
                        trading_type_element = "رهن کامل"
                    elif "خرید و فروش" in trade_type:
                        trading_type_element = "خرید و فروش"
                    elif "پیش فروش" in trade_type:
                        trading_type_element = "پیش فروش"
                    elif "مشارکت در ساخت" in trade_type:
                        trading_type_element = "مشارکت در ساخت"

                property_type_element = item_element[1].text

                for property_type in item_element[1]:
                    if "آپارتمان" in property_type:
                        property_type_element = "آپارتمان"
                    elif "ویلائی - زمین" in property_type:
                        property_type_element = "ویلائی - زمین"
                    elif "دفتر کار" in property_type:
                        property_type_element = "دفتر کار"
                    elif "مغازه" in property_type:
                        property_type_element = "مغازه"
                    elif "باغ و زمین زراعی" in property_type:
                        property_type_element = "باغ و زمین زراعی"
                    elif "انبار" in property_type:
                        property_type_element = "انبار"
                    elif "سوله" in property_type:
                        property_type_element = "سوله"

                # Getting Price

                if item_detail.find('h5') is not None:
                    price_elements = item_detail.find('h5').text
                    for trade in item_element[1]:
                        if "رهن واجاره" in trade:
                            rent_element = item_detail.find('h6').text
                            mortgage_fee = price_elements.replace(',', '').replace('رهن :', '').replace('تومان',
                                                                                                        '').replace(
                                ' ',
                                '')
                            rent_fee = rent_element.replace(',', '').replace('اجاره :', '').replace('تومان',
                                                                                                    '').replace(' ',
                                                                                                                '')
                        elif "خرید و فروش" or "رهن کامل" in trade:

                            price_fee = price_elements.replace(',', '').replace('رهن کامل', '').replace('تومان',
                                                                                                        '').replace(
                                "مبلغ فروش", '').replace(' ',
                                                         '')

                description_element = soup_detail.find('div', class_='DescMelk1').text.replace('توضیحات ملک :',
                                                                                               '').replace(
                    '//', ' ')

                description = description_element

                # Getting phone number

                owner_element = soup_detail.find('div', class_='DescMelk').find_all("h4")
                phone_element = owner_element[2].text.replace(' ', '').replace('\n', '')
                phone_number = (''.join(filter(str.isdigit, phone_element)))
                phone = phone_number

                feature = soup_detail.find('div', class_='Facilities')
                feature_values = feature.find_all('li')
                elevator = 0
                parking = 0
                for feature_value in feature_values:
                    feature_text = feature_value.text
                    if " آسانسور  " == feature_text:
                        elevator = 1
                    elif " پارکینگ  " == feature_text:
                        parking = 1
                    else:
                        additional_data[feature_text] = "دارد"
                yield {
                    'address': address_element,
                    'title': title,
                    'description': description,
                    'token': token,
                    'elevator': elevator,
                    'parking': parking,
                    'meter': meter,
                    'mortgage': mortgage_fee,
                    'rent': rent_fee,
                    'price': price_fee,
                    'phone': phone,
                    'property_type': property_type_element,
                    'trading_type': trading_type_element,
                    'url': url,
                    'additional_data': additional_data, }

            page_number += 1
        deactivate_abs24_session(authentication)
    except BaseException as ex:
        deactivate_abs24_session(authentication)
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(traceback.extract_tb(ex_traceback))
