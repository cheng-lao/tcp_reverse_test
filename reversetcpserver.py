import argparse
from threading import Thread
import socket
import time

def argsparse():
    parameters = argparse.ArgumentParser(description="Reverse TCP Server")
    parameters.add_argument("-p","--port",type=int,help="The port of the server",default=8080, required=True)
    parameters.add_argument("-l","--listen",type=int,help="The number of the server listen",default=50)
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
            if types == "00":
                cnt = int(data[2:]) # 此时是初始化报文， 生成的报文内容是发送的块数
                message = agreementMessage()
                Server.send(message.encode())   # 发送回应报文
                break
            else :continue
        for i in range(cnt):
            message = Server.recv(10240)
            message = message.decode()
            types = message[0:2]
            content = message[6:]
            content = content[::-1]
            response = reverseResponseMessage(content)  # 生成反转报文
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
    server.listen(args.listen)  # 最大连接数
    while True:
        client,addr = server.accept()   # 接受连接
        print(f"Connection from {addr}")    # 打印连接信息
        ClientPool[addr] = client       # 向池子当中增加一个客户端
        client_handler = Thread(target=handle_client,args=(client,))    # 创建一个线程
        client_handler.daemon = True    # 设置为守护线程
        client_handler.start()        # 启动线程
        
    

if __name__ == "__main__":
    server = None
    BlockNum = {}
    ClientPool = {}
    args = argsparse()
    main(args)
