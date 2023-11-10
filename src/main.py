import requests
from bs4 import BeautifulSoup
from enum import Enum
import re
url = 'https://www.nesdev.org/obelisk-6502-guide/reference.html'
response = requests.get(url)

class OpCodeData:
    
    def __init__(self, code, mnemonic, len, cycles, mode): #initializer
        self.code = code.replace('$','').strip()
        self.mnemonic = mnemonic
        self.len = len.strip()
        self.cycles = cycles.replace('(',' /*').replace(')','*/').strip()
        self.mode = mode.replace('(', '').replace(')', '').replace(',','_').replace(' ','').replace('Implied','NoneAddressing').strip()
    




if response.status_code == 200:
    # リクエスト成功
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    #mnemonic(LDAなど)を全件取得、リスト化
    h3List = soup.find_all('h3') #<h3>タグのlist
    mnemonic = []#mnemonic(LDAなど)のみのlist
    opcodedata = [] #classのOpCodeDataのlist
    for op in h3List:
        mnemonic.append(op.find('a').get('name'))
    mnemonicLen = len(mnemonic) #mnemonicのlength
    
    #tableを取得
    table = soup.find_all('table')
    #mnemonic全件分、AddressingModeを取得する
    for op in range(mnemonicLen):
        pos = 2 * (op + 1) #AdressingModeのテーブルはサイトで2つ飛ばしで出現する。
        adrmd = table[pos].find_all("tr")

        for a in adrmd[1:]: #table内のテキストの整形
            tbl_elm = a.find_all('td')
            adrmd = a.find('a').get_text()
            opcodedata.append(OpCodeData(tbl_elm[1].get_text(),mnemonic[op],tbl_elm[2].get_text(),tbl_elm[3].get_text(),adrmd))
    
    #できたOpCodeDataをtxtファイルに保存する。
    f = open('opcode.txt', 'w')
    for data in opcodedata:
        apdstr = 'OpCode::new(0x' + data.code +', \"' + data.mnemonic + '\", ' + data.len + ', ' + data.cycles +', AddressingMode::' + data.mode + '),'
        out = ''.join(char for char in apdstr if not char.isspace())
        f.write('\t\t'+ out + '\n')
    f.close()

    #なんかよくわからん改行が挟まってまじでうざい

else:
    # エラー処理
    print("error")