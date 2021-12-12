import socket, ssl

def client(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    #第一个参数表示上下文对象为客户端所用，用于验证其连接的服务器，
    #cafile选项表示脚本验证远程证书时信任的证书机构
    context = ssl.create_default_context(purpose, cafile=cafile)    
    context.check_hostname = False
    context.verify_mode=ssl.CERT_NONE
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('start')
    raw_sock.connect((host,port))
    print('Connected to host {!r} and port {}'.format(host, port))
    #参数调用的是已经使用connect()连接的主机名
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    return ssl_sock