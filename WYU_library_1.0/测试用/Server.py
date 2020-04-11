'''
服务端，测试用
'''


import socket
import threading
from time import ctime

#定义IP和端口号
HOST,POST = '',6666

#缓冲区
BUFFER_SIZE = 1024
ADDR = (HOST,POST)

#s数据
list1 = ['2019-11-02','casca','cascvasv vas','擦书废弃物·1','csd31cw5ef4q65f fq6w1a f14f6', 'fas5f山东潍坊', 'f4we6f5sfd f156']
end = "-1"
    
def deal_data(conn, addr):
    while True:
        # 接收1024个字节,并解码（bytes->str）
        data = conn.recv(BUFFER_SIZE).decode()
        if not data: 
            break
        print('学号：', data[0:10])
        print('密码：', data[10:])

        for i in range(len(list1)):
            conn.send(list1[i].encode())
            print(list1[i])
        conn.sendall(end.encode())
        print("数据已发送")
        break

        conn.close()
        print("已断开连接的客户端对象：",addr)
        print("\n")


def socket_service():
    #创建服务器套接字 AF_INET:IPv4,SOCK_STREAM:协议
    tcpServerSocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #绑IP和端口号
    tcpServerSocker.bind(ADDR)

    #监听最大连接数
    tcpServerSocker.listen(2)
    print("等待连接...")

    while True:
        #阻塞直到有连接为止，有了一个新连接进来后，就会为这个请求生成一个连接对象
        tcpClientSocket, client_addr = tcpServerSocker.accept()
        print("连接服务器的客户端对象：",client_addr)
        #t = threading.Thread(target=deal_data, args=(tcpClientSocket, client_addr))
        #t.start() 
        deal_data(tcpClientSocket, client_addr)


socket_service() 
    