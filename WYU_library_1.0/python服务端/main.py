'''
这里开始
接收学号、密码
在 data_process.py登录获得数据
传回数据
'''



import socket
import threading
from time import ctime
import time
from data_process import Data_process

def deal_data(conn, addr):
    while True:
        # 接收1024个字节,并解码（bytes->str）
        data =conn.recv(1024).decode()
        if not data:                 
            break
        
        print('学号：', data[0:10])
        print('密码：', data[10:])

        #将得到的学号，密码,验证码发送到图书馆网站，得到数据
        dataPro = Data_process(data)
        dataPro.login(dataPro)
        print("登录成功！正在获取数据...")
        list1 = dataPro.lscx(dataPro)

        #time.sleep(100)

        #将数据返回到客户端
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                conn.send(list1[i][j].encode())

        #结束符，若接收到这个数据就关闭客户端
        end = "-1"
        conn.sendall(end.encode())
        print("数据已发送")
        break

        conn.close()
        print("已断开连接的客户端对象：",addr)
        print("\n")


def socket_service():
    #定义IP和端口号
    HOST,POST = '',6666
    ADDR = (HOST,POST)

    #创建服务器套接字 AF_INET:IPv4,SOCK_STREAM:协议
    tcpServerSocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #绑定IP和端口号
    tcpServerSocker.bind(ADDR)

    #监听最大连接数
    tcpServerSocker.listen(2)
    print("等待连接...")

    while True:
        #阻塞直到有连接为止，有了一个新连接进来后，就会为这个请求生成一个连接对象
        tcpClientSocket, client_addr = tcpServerSocker.accept()
        print("连接服务器的客户端对象：",client_addr) 

        #开启线程处理数据
        t = threading.Thread(target=deal_data, args=(tcpClientSocket, client_addr))
        t.start()
        #deal_data(tcpClientSocket, client_addr)

if __name__ == "__main__":
    socket_service()