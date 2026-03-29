import socket
from datetime import datetime

# 创建套接字，使用IPV4协议，UDP传输
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except Exception as e:
    print(f'创建套接字失败：{e}')
    exit()

# 绑定本机所有IP + 端口5006（可修改为其他端口）
bind_addr = ('', 5006)
try:
    sock.bind(bind_addr)
except Exception as e:
    print(f'绑定端口失败（端口可能被占用）：{e}')
    exit()

print(f'时间服务器已启动，监听 {bind_addr} ...')
try:
    while True:
        # 接收客户端消息（缓冲区100字节）
        data, addr = sock.recvfrom(100)
        print(f'收到来自 {addr} 的消息：{data}')
        
        # 仅响应指定请求
        if data == b'ask for time':
            now = str(datetime.now())[:19]  # 截取到秒级
            sock.sendto(now.encode('utf-8'), addr)
            print(f'已向 {addr} 发送时间：{now}')
except KeyboardInterrupt:
    print('\n服务器已手动停止')
finally:
    sock.close()