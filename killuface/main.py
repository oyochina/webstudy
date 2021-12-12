import getcode,time
import network, send01_A,send02_A,send03_A,send04_A,send05_A,send06_A,vip_A


 #以下数据为打卡用 
maninfo={'刘圣豪':'17530000051164','张兵':'17530000051310'} 
#perid='17530000051164'#汇龙刘圣豪
#perid='17530000107236'#家里刘圣豪 

position_name="home"  
name='刘圣豪'
#name='郭可'#
perid=maninfo[name]

a='2021 10 11 11 35 12'
fmt='%Y %m %d %H %M %S'
t=time.mktime(time.strptime(a,fmt))
showtime=str(round(t * 1000))

#url='uniubi-aiot.oss-cn-hangzhou.aliyuncs.com/device/84E0F4286799527A/20210913082823_693_rgb.jpg'
url='uniubi-aiot.oss-cn-hangzhou.aliyuncs.com/device/84E0F4286799527A/20211011084127_373_rgb.jpg'
#url='uniubi-aiot.oss-cn-hangzhou.aliyuncs.com/device/84E0F42867B8527A/20210909173933_127_rgb.jpg'#园区
#url='uniubi-aiot.oss-cn-hangzhou.aliyuncs.com/device/84E0F42650E11501/20210916203036_470_rgb.jpg'
#url='uniubi-aiot.oss-cn-hangzhou.aliyuncs.com/device/84E0F42867D8527A/20210924172815_055_rgb.jpg'
#获取原始发送数据（列表，元素为带\x的字符串）
all_data=[]
if position_name=="home":
    all_data=getcode.read_code("./data/main_home.txt")
    card0,card1=getcode.read_card("./data/card_home.txt")
elif position_name=="园区":
    all_data=getcode.read_code("./data/main_yq.txt")
    card0,card1=getcode.read_card("./data/card_yq.txt")
elif position_name=="主楼左":
    all_data=getcode.read_code("./data/main_left.txt")
    card0,card1=getcode.read_card("./data/card_left.txt")
elif position_name=="主楼右":
    all_data=getcode.read_code("./data/main_right.txt")
    card0,card1=getcode.read_card("./data/card_right.txt")

pk00=80 #大包号初始号
pk01=80#把第几个包解析出来,小包初始号
newdata0,newdata1=send01_A.makedata(pk00,pk01,all_data[0],all_data[1])  #生成第1个数据包
#newdata2,newdata3=send02_A.makedata(pk00,pk01,all_data[2],all_data[3])
#newdata4,newdata5=send03_A.makedata(pk00,pk01,all_data[4],all_data[5])
#newdata6,newdata7=send04_A.makedata(pk00,pk01,all_data[6],all_data[7])
#newdata8,newdata9=send05_A.makedata(pk00,pk01,all_data[8],all_data[9])
#newdata10,newdata11,num1,num2=send06_A.makedata(pk00,pk01,all_data[10],all_data[11])
#newdata12,newdata13,heart00,heart01=vip_A.makedata(pk00=50,pk01=50,perid=perid,name=name,showtime=showtime,url=url,title0=card0,title1=card1)
#print('hello')



#newdata2,newdata3,heart00,heart01=vip_A.makedata(pk00=50,pk01=50,perid=perid,name=name,showtime=showtime,url=url,card0=card0,card1=card1)
#print(newdata2)
#print(newdata3)
#print('hello')

#发送第1个数据包
serv_ip=['121.43.225.177','114.215.200.46']
ssl_sock=network.client(serv_ip[1],50980)
ssl_sock.sendall(newdata0)
time.sleep(0.005)
ssl_sock.sendall(newdata1)


#收到响应后开始
i=0 #发包次数
j=0 #收包次数
heart00=0
heart01=0
n=100 #第n个包开始打卡
while True:
    data = ssl_sock.recv(2048)
    j=j+1
    if not data:
        break
    print(repr(data))
    if i==0:
        newdata0,newdata1=send02_A.makedata(pk00,pk01,all_data[2],all_data[3])  #回包有2个  
        ssl_sock.sendall(newdata0)
        time.sleep(0.005)
        ssl_sock.sendall(newdata1)
        i=i+1
    elif i==1 and j==3 : #收到3个包后3个包连发
        newdata0,newdata1=send03_A.makedata(pk00,pk01,all_data[4],all_data[5])    
        ssl_sock.sendall(newdata0)
        time.sleep(0.001)
        ssl_sock.sendall(newdata1)
        i=i+1
        
        newdata0,newdata1=send04_A.makedata(pk00,pk01,all_data[6],all_data[7])    
        ssl_sock.sendall(newdata0)
        time.sleep(0.001)
        ssl_sock.sendall(newdata1)
        i=i+1   

        newdata0,newdata1=send05_A.makedata(pk00,pk01,all_data[8],all_data[9]) 
        ssl_sock.sendall(newdata0)
        time.sleep(0.001)
        ssl_sock.sendall(newdata1)
        i=i+1 
        print('3包连发完成')
        heart00=pk00+5
        heart01=pk01+4
    elif i>3 and i!=n:
        time.sleep(10)
        newdata0,newdata1,heart00,heart01=send06_A.makedata(heart00,heart01,all_data[10],all_data[11])
        ssl_sock.sendall(newdata0)
        time.sleep(0.001)
        ssl_sock.sendall(newdata1)
        i=i+1 #第1个心跳包 
    elif i==n: #打卡
        time.sleep(10)        
        newdata0,newdata1,heart00,heart01=vip_A.makedata(pk00=heart00,pk01=heart01,perid=perid,name=name,showtime=showtime,url=url,title0=card0,title1=card1)
        ssl_sock.sendall(newdata0)
        time.sleep(0.001)
        ssl_sock.sendall(newdata1)
        print('打卡完成')
        i=i+1 #第1个心跳包 

