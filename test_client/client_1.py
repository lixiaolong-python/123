#!/usr/bin/python
# coding:utf-8
# client.py
from socket import *
from time import ctime
# from termios import tcflush,TCIFLUSH
import threading
import sys

HOST = '42.159.80.130'
PORT = 8883
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
'''
因为每个客户端接收消息和发送消息是相互独立的，
所以这里将两者分开，开启两个线程处理
'''


def Send(sock, test):
    while True:
        try:
            data = input("请输入\n：")
            sock.send(data)
            if data == 'Quit':
                break
        except KeyboardInterrupt:
            sock.send('Quit')
            break


def Recv(sock, test):
    while True:
        data = sock.recv(BUFSIZ)
        if data == 'Quit.':
            print('He/She logout')
            continue
        if data == 'Quit':
            break
        print('			%s' % data)


if __name__ == '__main__':
    print('链接成功')
    while True:
        username = input('Your name(press only Enter to quit): ')
        username = username.encode('utf-8')
        tcpCliSock.send(username)

        if not username:
            break
        # username is not None
        response = tcpCliSock.recv(1024)
        print(response)

    if not username:
        tcpCliSock.close()

    recvMessage = threading.Thread(target=Recv, args=(tcpCliSock, None))
    sendMessage = threading.Thread(target=Send, args=(tcpCliSock, None))
    sendMessage.start()
    recvMessage.start()
    sendMessage.join()
    recvMessage.join()







#----------------------------------------------------------------


# # tcp客户端
#
# from socket import *
#
# # 1创建套接字
# tcp_socket = socket(AF_INET, SOCK_STREAM)
#
# # 2绑定端口
# # ip = input('请输入要连接服务器ip：')
# # port = int(input('请输入要连接服务器端口：'))
#
# # 3连接服务器
# # IP = "http://192.168.22.233:9999"
#
# ip = "42.159.80.130"
# port = 8883
#
# # ip = "42.159.80.130"
# # port = 9999
#
# tcp_socket.connect((ip, port))
#
#
# while True:
# # 4发送接收数据
#     send_data = input('B我是客户- _ - \n请输入要传送数据：')
#     send_data = send_data.encode('utf-8')
#     tcp_socket.send(send_data)
#
#     recv_data = tcp_socket.recv(1024)
#     recv_data = recv_data.decode('utf-8')
#     print(recv_data)
#
# # 5关闭套接字
# tcp_socket.close()

#  先发这个
#  02010f000600000000013938313130333439383131303334353e0d0a

# 应该有返回值，告诉我是谁发的

#  在发这个
#  050f170037010100010009556af64    0e64440000000000000000000000000010100490d0a