import socket
import sys
import os  # 处理Windows路径分隔符
"""
运行环境配置
操作系统：Windows 10/11
Python
仅使用Python标准库socket、sys
网络要求：服务器与客户端需在同一网络，关闭防火墙
配置选项说明
监听端口：通过命令行参数指定（1-65535之间的整数）
接收缓冲区大小：固定1024字节（可用recvfrom(1024)调整，需与客户端分块大小一致）
文件名前缀：接收文件自动添加"recv"前缀
超时设置：接收文件名时超时5秒
github作业提交处： https://github.com/sheldon-wjc/udp-file-transfer.git
"""
def main():
    #  从命令行获取参数（serverIP、serverPort、filepath）
    if len(sys.argv) != 4:
        print("用法: python udpclient.py <serverIP> <serverPort> <filepath>")
        sys.exit(1)
    serverip = sys.argv[1]
    serverport = int(sys.argv[2])
    filepath = sys.argv[3]

    # Windows路径分隔符（将\转为/，避免文件名解析错误）
    filepath = filepath.replace('\\', '/')

    # 2. 创建UDP套接字，设置5秒超时
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientsocket.settimeout(5)

    try:
        # 模拟TCP三次握手
        print("正在尝试与服务器建立连接...")
        clientsocket.sendto(b'cwjc-hello', (serverip, serverport))
        response, serveraddr = clientsocket.recvfrom(1024)
        if response.decode() == 'swjc-hello':
            print("已与服务器建立连接！")
        else:
            print("连接建立失败，服务器响应异常")
            return

        # 传输文件
        print(f"开始传输文件: {filepath}")
        # 解析文件名
        filename = filepath.split('/')[-1].encode()
        clientsocket.sendto(filename, serveraddr)

        # 逐段发送文件内容
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                clientsocket.sendto(data, serveraddr)
        print("文件传输完成！")

        # 模拟TCP四次挥手
        print("正在关闭连接...")
        clientsocket.sendto(b'bye', serveraddr)
        closeresp, _ = clientsocket.recvfrom(1024)
        if closeresp.decode() == 'bye':
            print("连接已关闭")
        else:
            print("连接关闭异常")

    except socket.timeout:
        print("操作超时，服务器未响应（检查服务器是否启动/端口是否正确）")
    except FileNotFoundError:
        print(f"错误：文件 {filepath} 不存在（请检查文件路径）")
    except Exception as e:
        print(f"客户端异常: {e}")
    finally:
        clientsocket.close()

if __name__ == "__main__":
    main()