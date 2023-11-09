import requests
from bs4 import BeautifulSoup

url = 'https://www.nesdev.org/obelisk-6502-guide/reference.html'
response = requests.get(url)

if response.status_code == 200:
    # リクエスト成功
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_op = soup.find_all('h3')
    for i in h3_op:
        print(i.find('a').get('name'))
    
else:
    # エラー処理
    print(f"Error: {response.status_code}")