import requests
from bs4 import BeautifulSoup
from enum import Enum
url = 'https://www.nesdev.org/obelisk-6502-guide/reference.html'
response = requests.get(url)

class AddressingMode(Enum):
    Immediate = 0
    ZeroPage = 1
    ZeroPage_X = 2
    ZeroPage_Y = 3
    Absolute = 4
    Absolute_X = 5
    Absolute_Y = 6
    Indirect_X = 7
    Indirect_Y = 8
    NoneAddressing = 9

class OpCodeData:
    
    def __init__(self, code, mnemonic, len, cycles, mode): #initializer
        self.code = code.replace('$','')
        self.mnemonic = mnemonic
        self.len = len
        self.cycles = cycles.replace(' ','').replace('(','/*').replace(')','*/')
        self.mode = mode.replace('(', '').replace(')', '').replace(',','_').replace(' ','').replace('Implied','NoneAdressing')
    




if response.status_code == 200:
    # リクエスト成功
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_op = soup.find_all('h3')
    opcode_code = []
    opcodedata = []
    for op in h3_op:
        opcode_code.append(op.find('a').get('name'))
    table = soup.find_all('table')
    #print(table[2].find('tr'))
    opc_len = len(opcode_code)
    for op in range(opc_len):
        pos = 2 * (op + 1)
        zero = 0
        adrmd = table[pos].find_all("tr")
        #print(len(adrmd))
        for a in adrmd[1:]:
            tbl_elm = a.get_text().split('\n')
            #print(a.get_text().split('\n')) #1->mode,3->code,5->bytes,6->cycles
            #print("Kobo Kanaeru:犬は好きですか？")
            adrmd = a.find('a').get_text().replace('\n','')
            opcodedata.append(OpCodeData(tbl_elm[3],opcode_code[op],tbl_elm[5],tbl_elm[6],adrmd))
    f = open('opcode.txt', 'w')
    for data in opcodedata:
        f.write('OpCode::new(0x' + data.code +', \"' + data.mnemonic + '\", ' + data.len + ', ' + data.cycles +', AddressingMode::' + data.mode + '),\n')
else:
    # エラー処理
    print("error")