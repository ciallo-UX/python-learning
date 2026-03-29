import socket
from time import sleep

# 服务器地址（关键！改为你的服务器IP+端口）
SERVER_IP = '127.0.0.1'  # 同一台机器用127.0.0.1；局域网用服务器内网IP（如192.168.8.141）
SERVER_PORT = 5006

while True:
    try:
        # 创建UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)  # 超时时间0.5秒
        
        # 发送请求
        sock.sendto(b'ask for time', (SERVER_IP, SERVER_PORT))
        
        # 接收响应
        try:
            data, addr = sock.recvfrom(100)
            print(f'服务器时间：{data.decode("utf-8")}')
        except socket.timeout:
            print('未收到服务器响应（服务器可能未启动/IP/端口错误/网络不通），1秒后重试...')
        except Exception as e:
            print(f'接收数据失败：{e}')
    except Exception as e:
        print(f'创建套接字失败：{e}')
        break
    finally:
        sock.close()
        sleep(1)  # 每秒请求一次