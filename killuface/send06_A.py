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
    #pk00=pk00+5
    #pk01=pk01+6
    #title0=b'\x00\x00\x3e\x00\x00\x00\x00\x2e'
    #title1=b'\x12\x21\x38\x34\x45\x30\x46\x34\x32\x36\x35\x30\x45\x31\x31\x35\x30\x31\x31\x36\x33\x30\x31\x35\x32\x39\x39\x39\x38\x35\x30\x30\x30\x35\x36\x18\xaa\x87\xc3\xe5\xb8\x2f\x22\x02\x08\x01'

    t = time.time()#生成时间戳
    nowtime=str(round(t * 1000))
    title2=title1.replace(title1[18:31],str2xstr(nowtime)) #改了时间

    #小包初始号
    pk01_str=str(pk01)
    if len(str(pk01))==1:
        pk01_str='000'+pk01_str
    elif len(str(pk01))==2:
        pk01_str='00'+pk01_str
    elif len(str(pk01))==3:
        pk01_str='0'+pk01_str        
    title3=title2.replace(title1[31:35],str2xstr(pk01_str) ) #改包号

    #重新封装(小包)
    newdata1=xstr2byte(title3)

    #封装大包数据
    newdata0=xstr2byte(title0[0:2])+struct.pack('H',pk00) +struct.pack('!I',len(title3)) #根据小包生成大包数据
    
    pk00=pk00+1
    pk01=pk01+1
    return  newdata0,newdata1,pk00,pk01