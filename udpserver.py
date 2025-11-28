import socket
import sys

def main():
    # 1. 从命令行获取参数：监听端口
    if len(sys.argv) != 2:
        print("用法: python udpserver.py <listen_port>")
        sys.exit(1)
    listenport = int(sys.argv[1])

    # 2. 创建UDP套接字并绑定端口（关闭超时，避免误判）
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind(('', listenport))
    print(f"服务器已启动，监听端口 {listenport}...")

    try:
        # 模拟TCP连接建立（三次握手简化版）
        connreq, clientaddr = serversocket.recvfrom(1024)
        if connreq.decode() == 'cwjc-hello':
            print(f"收到客户端 {clientaddr} 的连接请求")
            serversocket.sendto(b'swjc-hello', clientaddr)
            print(f"已与客户端 {clientaddr} 建立连接")
        else:
            print("收到无效的连接请求，忽略")
            return

        # 接收文件名（设置10秒超时，确保能收到文件名）
        serversocket.settimeout(10)
        try:
            filename, _ = serversocket.recvfrom(1024)
            filename = filename.decode().strip()  # 去除可能的空格/换行
            print(f"开始接收文件: {filename}")
        except socket.timeout:
            print("接收文件名超时，连接关闭")
            return
        finally:
            serversocket.settimeout(None)  # 取消超时，持续接收文件数据

        # 接收文件内容（仅当收到'bye'时才结束）
        with open(f"recv_{filename}", 'wb') as f:
            print("正在接收文件内容...（等待客户端发送完成）")
            while True:
                data, addr = serversocket.recvfrom(1024)
                # 验证数据来自已连接的客户端（UDP无连接，需手动校验）
                if addr != clientaddr:
                    continue
                # 收到'bye'说明文件传输完成，退出循环
                if data.decode() == 'bye':
                    print("文件内容接收完成（收到关闭指令）")
                    break
                f.write(data)

        print(f"文件已保存为: recv_{filename}")

        # 模拟TCP双向挥手
        serversocket.sendto(b'bye', clientaddr)
        print(f"已与客户端 {clientaddr} 关闭连接")

    except Exception as e:
        print(f"服务器异常: {e}")
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()