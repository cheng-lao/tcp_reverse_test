import os
import argparse
from threading import Thread
import socket
import time

def argsparse():
    parameters = argparse.ArgumentParser(description="Reverse TCP Server")
    parameters.add_argument("-p","--port",type=int,help="The port of the server",default=8080, required=True)
    parameters.add_argument("-l","--listen",type=int,help="The number of the server listen",default=5)
    args = parameters.parse_args()
    return args

def agreementMessage():
    # 生成agreement报文
    types = "01"
    message = types
    return message

def reverseResponseMessage(content: str):
    types = "11"
    message = types + str(len(content)).zfill(4) + content
    return message


def handle_client(Server:socket.socket):
    global BlockNum
    try:
        while True:
            data = Server.recv(10240)
            data = data.decode()
            types = data[0:2]
            # content = data[6:]
            if types == "00":
                # 此时是初始化报文
                # 生成的报文内容是发送的块数
                cnt = int(data[2:])
                # 发送回应报文
                message = agreementMessage()
                Server.send(message.encode())
                # time.sleep(0.0001)  # 休眠一下 等待发送
                break
            else :continue
        for i in range(cnt):
            message = Server.recv(10240)
            message = message.decode()
            types = message[0:2]
            content = message[6:]
            # print(f"收到的消息: {content}")
            content = content[::-1]
            response = reverseResponseMessage(content)
            # print(f"发送的消息: {content}")
            Server.send(response.encode())
            time.sleep(0.001)
    except Exception as e:
        print(e)
    finally:
        print("Close Connection:",Server)
        time.sleep(10)
        Server.close()
        


def main(args):
    global server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("172.19.73.224",args.port))
    server.listen(args.listen)
    while True:
        client,addr = server.accept()
        print(f"Connection from {addr}")
        ClientPool[addr] = client       # 向池子当中增加一些增加
        client_handler = Thread(target=handle_client,args=(client,))
        client_handler.daemon = True
        client_handler.start()
        
    

if __name__ == "__main__":
    server = None
    BlockNum = {}
    ClientPool = {}
    args = argsparse()
    main(args)






