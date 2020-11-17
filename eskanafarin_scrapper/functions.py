import requests
from bs4 import BeautifulSoup


def login_session_abs24(username, password):
    url = "https://abs24.ir/index.php"

    payload = {'txtu': username, 'txtp': password, 'enter1': 'ورود'}
    files = []

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://abs24.ir',
        # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryEFzdCPXpeC5iwgWw',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    }

    response = requests.post(url, headers=headers, data=payload, files=files)

    soup = BeautifulSoup(response.content, 'lxml')
    valid_session = response.cookies.get('PHPSESSID')

    return valid_session


def deactivate_abs24_session(session):
    url = "https://abs24.ir/index.php?out=1"

    payload = {}
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cookie': 'PHPSESSID=' + str(session)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
