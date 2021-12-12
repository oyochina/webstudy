#wiresharkc中数据(C Arrays)保存后读取，用正则表达式提取发送数据，整理成二进制进制数据（16进制显示）
import re,struct, codecs

def xstrtobyte(thestr):
    aa=[ord(c) for c in thestr]
    #print(aa)
    return struct.pack(str(len(aa))+'B',*aa)

def read_code(path="./主楼carrays.txt"):#返回接发送据包列表，列表为带\x的字符串
    str_all=''
    with open(path,'r',encoding='utf8') as file:
        for line in file:
            str_all+=line.strip("\n")
    
    #构造正则表达式
    pattern = re.compile(r'char peer0_\d+\[\] = { \/\*.+?\*\/(.+?)}')
    data = pattern.findall(str_all)
    data_new=[]
    for m in data:
        #data_new.append(m.replace(', ', '').replace(' ','').replace('0x',r'\x'))
        #mm=m.replace(', ', '').replace(' ','')
        mm=m.replace(', ', '').replace(' ','').replace('0x',r'\x')
        data_new.append(codecs.decode(mm, "unicode_escape"))
    return data_new

def read_card(path="./打卡数据.txt"):
    i=0
    str_first=''
    str_data=''
    with open(path,'r',encoding='utf8') as file:
        for line in file:
            if i==0:
                str_first=line[10:33]
                i=i+1
            else:
                str_data+=line[10:59]
    mm=r'\x'+str_first.replace(' ',r'\x')
    mm_first=codecs.decode(mm, "unicode_escape")

    #构造正则表达式
    pattern = re.compile('(\s+)$')
    data = pattern.findall(str_data)
    new_data=str_data.replace(data[0],'')

    mm=r'\x'+new_data.replace('  ',r' ').replace(' ',r'\x')

    

    mm_data=codecs.decode(mm, "unicode_escape")

    return  mm_first,mm_data 
            


if __name__ == '__main__':
    print(read_code('./data/main_left.txt')[1])
    #mm_first,mm_data=read_card()
    #print(mm_first)
    #print(mm_data)