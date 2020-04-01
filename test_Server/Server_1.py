#!/usr/bin/python
# coding:utf-8
# server.py
from socket import *
from time import ctime
import threading
import re

HOST = ''
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

clients = {}  # username -> socket
chatwith = {}  # user1.socket -> user2.socket


# clients字典中记录了连接的客户端的用户名和套接字的对应关系
# chatwith字典中记录了通信双方的套接字的对应

# messageTransform()处理客户端确定用户名之后发送的文本
# 文本只有四种类型：
#	None
#   Quit
#	To:someone
#	其他文本
def messageTransform(sock, user):
    while True:
        data = sock.recv(BUFSIZ)
        if not data:
            if chatwith.has_key(sock):
                chatwith[sock].send(data)
                del chatwith[chatwith[sock]]
                del chatwith[sock]
            del clients[user]
            sock.close()
            break
        if data == 'Quit':
            sock.send(data)
            if chatwith.has_key(sock):
                data = '%s.' % data
                chatwith[sock].send(data)
                del chatwith[chatwith[sock]]
                del chatwith[sock]
            del clients[user]
            sock.close()
            break
        elif re.match('^To:.+', data) is not None:
            data = data[3:]
            if clients.has_key(data):
                if data == user:
                    sock.send('Please don\'t try to talk with yourself.')
                else:
                    chatwith[sock] = clients[data]
                    chatwith[clients[data]] = sock
            else:
                sock.send('the user %s is not exist' % data)
        else:
            if chatwith.has_key(sock):
                chatwith[sock].send('[%s] %s: (%s)' % (ctime(), user, data))
            else:
                sock.send('Nobody is chating with you. Maybe the one talked with you is talking with someone else')


# 每个客户端连接之后，都会启动一个新线程
# 连接成功后需要输入用户名
# 输入的用户名可能会：
#	已存在
#	(客户端直接输入ctrl+c退出)
#	合法用户名
def connectThread(sock, test):  # client's socket

    user = None
    while True:  # receive the username
        username = sock.recv(BUFSIZ)
        if not username:  # the client logout without input a name
            print('The client logout without input a name')
            break
        if clients.has_key(username):  # username existed
            sock.send('Reuse')
        else:  # correct username
            sock.send('OK')
            clients[username] = sock  # username -> socket
            user = username
            break
    if not user:
        sock.close()
        return
    print('The username is: %s' % user)
    # get the correct username

    messageTransform(sock, user)


if __name__ == '__main__':
    while True:
        print('...WAITING FOR CONNECTION')
        tcpCliSock, addr = tcpSerSock.accept()
        print('CONNECTED FROM: ', addr)
        chat = threading.Thread(target=connectThread, args=(tcpCliSock, None))
        chat.start()











#--------------------------------------------------------------------------------------------
# # 1创建套接字
# import socket
# tcp_socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#
# # 服务器端口回收操作（释放端口）
# tcp_socket_host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
#
# # 2绑定端口
# tcp_socket_host.bind(('127.0.0.1', 8080))
#
# # 3监听  变为被动套接字
# tcp_socket_host.listen(128)    # 128可以监听的最大数量，最大链接数
#
# # 4等待客户端连接
# socket_fuwu, addr_client = tcp_socket_host.accept()  # accept(new_socket, addr)
# print(socket_fuwu)
# print(addr_client)
# # 5读写
#
# while True:
#     recv_data = socket_fuwu.recv(1024)   #接收数据
#     print(recv_data.decode('utf-8'))
#
#     seng_data = input("A我是服务器- _ -\n服务器发送内容：")
#     # seng_data = "A我是服务器- _ -\n服务器发送内容："
#     socket_fuwu.send(seng_data.encode('utf-8'))  #发送数据
#
# # 6服务套接字关闭
# socket_fuwu.close()    # 服务器一般不关闭
