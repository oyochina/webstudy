import struct,time,codecs

def xstr2byte(thestr):
    aa=[ord(c) for c in thestr]
    #print(aa)
    return struct.pack(str(len(aa))+'B',*aa)

def str2xstr(str_chg):
    ss=''
    str_chg_b=str_chg.encode('utf-8')
    for pp in struct.unpack(str(len(str_chg_b))+'B',str_chg_b):
        ss=ss+hex(pp)
    xstr=codecs.decode(ss.replace('0x',r'\x'), "unicode_escape")#整理成\x形式
    #print(xstr2byte(xstr).decode('utf-8'))
    return xstr

def makedata(pk00,pk01,title0=None,title1=None):
    pk00=pk00+2
    pk01=pk01
    #title0='\x00\x00\x3c\x00\x00\x00\x00\x7e'
    #title1='\x08\x0a\x12\x21\x38\x34\x45\x30\x46\x34\x32\x36\x35\x30\x45\x31\x31\x35\x30\x31\x31\x36\x33\x30\x31\x35\x32\x39\x38\x39\x39\x33\x30\x30\x30\x35\x33\x18\xe1\xd2\xc2\xe5\xb8\x2f\x72\x50\x08\x01\x10\x01\x1a\x21\x38\x34\x45\x30\x46\x34\x32\x36\x35\x30\x45\x31\x31\x35\x30\x31\x31\x36\x33\x30\x31\x35\x32\x39\x38\x39\x39\x33\x30\x30\x30\x35\x33\x20\xe1\xd2\xc2\xe5\xb8\x2f\x28\xeb\xb6\xd6\xaf\x98\xfe\x03\x32\x10\x38\x34\x45\x30\x46\x34\x32\x36\x35\x30\x45\x31\x31\x35\x30\x31\x52\x06\x22\x04\x08\x04\x10\x08'
    
   

    #解包(小包)
    #b=struct.unpack('4s16s13s4s15s16s13s4s17s16s8s',title1) 
    # 4s 16s(sn) 13s(time) 4s(pknum) 15s(unknow) 16s(sn) 13s(time) 4s(pknum) 17s(unknow) 16s(sn) 8s(unknow)（tuple格式）


    t = time.time()#生成时间戳
    nowtime=str(round(t * 1000))    
    title2=title1.replace(title1[20:33],str2xstr(nowtime)) #改了时间1

    #小包初始号
    pk01_str=str(pk01)
    if len(str(pk01))==1:
        pk01_str='000'+pk01_str
    elif len(str(pk01))==2:
        pk01_str='00'+pk01_str
    elif len(str(pk01))==3:
        pk01_str='0'+pk01_str        
    title3=title2.replace(title1[33:37],str2xstr(pk01_str) ) #改包号1

    title4=title3.replace(title1[68:81],str2xstr(nowtime)) #改了时间2
    title5=title4.replace(title1[81:85],str2xstr(pk01_str) ) #改包号1


    #重新封装(小包)
    newdata1=xstr2byte(title5)

    #封装大包数据
    newdata0=xstr2byte(title0[0:2])+struct.pack('H',pk00) +struct.pack('!I',len(title5)) #根据小包生成大包数据

    return  newdata0,newdata1

if __name__ == '__main__':
    newdata0,newdata1=makedata(50,50)