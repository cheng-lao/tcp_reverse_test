import time
from threading import Thread
import os 
import argparse
import socket
import random

def argsparse():
    parser = argparse.ArgumentParser(description='Reverse TCP Client')
    parser.add_argument('-ip',"--serverip", default="172.19.73.224" ,help="Server IP Address", required=True)
    parser.add_argument('-p',"--port", type = int, default=12345, help="Server Port", required=True)
    parser.add_argument('-f',"--filepath", default="test.txt", help="File to send", required=True)
    parser.add_argument('-Lmin',"--MinSizeBlock", type = int , default= 1024 ,help="Minimum number of blocks to send and the Minimum can't smaller than the 1024", required=False)
    parser.add_argument('-Lmax',"--MaxSizeBlock", type = int , default= 1400 ,help="Maximum number of blocks to send and the Maximum can't bigger than the 1400", required=False)
    args = parser.parse_args()
    args.MinSizeBlock = 1024 if args.MinSizeBlock < 1024 else args.MinSizeBlock
    args.MaxSizeBlock = 1400 if args.MaxSizeBlock > 1400 else args.MaxSizeBlock
    if args.MinSizeBlock > args.MaxSizeBlock:
        parser.error("MinSizeBlock can't bigger than MaxSizeBlock")
    return args

def GetContent(TxTFilePath:str):
    global content
    with open(TxTFilePath, 'r') as f:
        content = f.read()

def IntilizationMessage():
    global FileSize
    global sendList
    # 初始化报文需要计算一下总共有多少块
    tyeps = "00"
    FileSize = len(content.encode())
    size = FileSize 
    index = 0

    while size!=0:
        if size < args.MinSizeBlock:
            # 如果小于最小块大小 直接将这部分作为最后的发送部分
            sendList.append(content[index : index + size])
            size = 0
            index = index + size
        else:
            randomsize = random.randint(args.MinSizeBlock,args.MaxSizeBlock)
            sendlen.append(randomsize)
            sendList.append(content[index : index + randomsize])
            size -= randomsize
            index = index + randomsize
    N = len(sendList)
    print("发送的总块数是 ",N)
    time.sleep(1)
    sendlen.append(args.MinSizeBlock)
    sendlen.append(args.MaxSizeBlock)
    message = tyeps + str(N).zfill(4)
    return message

def agreementMessage():
    # 生成agreement报文
    types = "01"
    message = types
    return message

def reverserRequestMessage(idx: int):
    """生成反向请求报文
    Args:
        idx (int): 发送的块的索引 sendList[idx]
    """
    types = "10"
    content = sendList[idx]
    message = types + str(len(content)).zfill(4)  + content
    return message

def GetReverseFilePath(filepath:str):
    filename = os.path.basename(filepath)
    path = os.path.dirname(filepath)
    ReversePath = os.path.join(path,"reverse_"+filename)
    if not os.path.exists(ReversePath):
        with open(ReversePath, 'w') as f:
            pass
    else :
        cnt = 0
        while True:
            ReversePath = os.path.join(path,"reverse_"+str(cnt)+filename)
            if not os.path.exists(ReversePath):
                with open(ReversePath, 'w') as f:
                    pass
                break
            else : cnt+=1
    return ReversePath
    # 获取目标文件路径

def run(client:socket,args):
    global ReceivedContent
    filepath = args.filepath
    ReversePath = GetReverseFilePath(filepath)
    try:
        for i in range(len(sendList)):
            message = reverserRequestMessage(i)
            client.send(message.encode())
            response = client.recv(10240)
            response = response.decode()
            # content = MessageTackle(response)
            content = response[6:]
            # types = response[0:2]
            print(f"第{i+1}块反转之后收到的的内容: {content}")
            ReceivedContent += content
    except ConnectionResetError as e:
        print("连接被重置",e) 
    finally :
        content = ReceivedContent
        with open(ReversePath, 'r+') as f:
            old = f.read()
            f.seek(0)
            f.write(content)
            f.write(old)
        client.close()
        print("All reversed content has been received and saved to ",ReversePath)

def main(args):
    GetContent(args.filepath)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP客户端连接
    client.connect((args.serverip, args.port))
    message = IntilizationMessage()
    client.send(message.encode())
    response = client.recv(10240)
    response = response.decode()
    if response == agreementMessage :
        print("Iitialization Success")
    run(client,args)


if __name__ == "__main__":
    start = time.time()
    FileSize = 0
    content = ""
    sendList = []
    sendlen = []
    ReceivedContent = ""
    args = argsparse()
    main(args)
    endtime = time.time()
    print("The Program Total time is ",endtime-start)



