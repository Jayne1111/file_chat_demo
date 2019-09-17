#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import user_req_login
import json
import os,sys


conf = json.load(open(r"C:\Users\lx\Documents\Visual Studio Code\聊天室\server_conf.json"))  # 加载配置信息
# dest_file_abs_path = os.path.abspath(sys.argv[1])
# dest_file_parent_path = os.path.dirname(dest_file_abs_path)
# dest_file_name = os.path.basename(dest_file_abs_path)

# UDP打洞
# 定长包头(15B) + 变长聊天消息(昵称:聊天内容)

def client_chat(sock_conn, client_addr):
    try:
        while True:
                msg_len_data = sock_conn.recv(15)
                if not msg_len_data:
                    break

                msg_len = int(msg_len_data.decode().rstrip())
                recv_size = 0
                msg_content_data = b""
                while recv_size < msg_len:
                    tmp_data = sock_conn.recv(msg_len - recv_size)
                    if not tmp_data:
                        break
                    msg_content_data += tmp_data
                    recv_size += len(tmp_data)
                else:
                    # 发送给其他所有在线的客户端
                    for sock_tmp, tmp_addr in client_socks: 
                        if sock_tmp is not sock_conn:
                            try:
                                sock_tmp.send(msg_len_data)
                                sock_tmp.send(msg_content_data)
                            except:
                                client_socks.remove((sock_tmp, tmp_addr))
                                sock_tmp.close()
                    continue
                break
    finally:
            client_socks.remove((sock_conn, client_addr))
            sock_conn.close()

def user_service_thread(sock_conn,client_addr):
    try:
        data_len = sock_conn.recv(15).decode().rstrip()
        if len(data_len) > 0:
            data_len = int(data_len)

            recv_size = 0
            json_data = b""
            while recv_size < data_len:
                tmp = sock_conn.recv(data_len - recv_size)
                if tmp == 0:
                    break
                json_data += tmp
                recv_size += len(tmp)
            
            json_data = json_data.decode()
            req = json.loads(json_data)

            if req["op"] == 1:
                # 登录校验
                rsp = {"op": 1, "error_code": 0}

                if user_req_login.check_uname_pwd(req["args"]["uname"], req["args"]["passwd"]):
                    rsp["error_code"] = 1
                
                header_data = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(header_data)).encode()
                sock_conn.send(data_len)
                sock_conn.send(header_data)

                if not rsp["error_code"]:
                    client_chat((sock_conn,client_addr))

            elif req["op"] == 2:
                # 用户注册
                rsp = {"op": 2, "error_code": 0}
                if not user_req_login.user_reg(req["args"]["uname"], req["args"]["passwd"], req["args"]["phone"], req["args"]["email"]):
                    # 注册失败
                    rsp["error_code"] = 1

                rsp = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(rsp)).encode()
                sock_conn.send(data_len)
                sock_conn.send(rsp)            

            elif req["op"] == 3:
                # 校验用户名是否存在
                rsp = {"op": 3, "error_code": 0}

                ret = user_req_login.check_user_name(req["args"]["uname"])
                if ret == 2:
                    rsp["error_code"] = 1
                
                rsp = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(rsp)).encode()
                sock_conn.send(data_len)
                sock_conn.send(rsp)            
    finally:
        print("客户端(%s:%s)断开连接！"% client_addr)
        sock_conn.close()


# def send_dir(sock_conn):
#     '''
#     发送非空文件夹
#     '''
#     for root, dirs, files in os.walk(dest_file_abs_path):
#         if len(dirs) == 0 and len(files) == 0:
#             send_empty_dir(sock_conn, root)
#             continue

#         for f in files:
#             file_abs_path = os.path.join(root, f)
#             print(file_abs_path)
#             send_one_file(sock_conn, file_abs_path)


client_socks = []


def main():
    global client_socks
    
    sock_listen = socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_listen.bind(("127.0.0.1", 9999))
    sock_listen.listen(5)

    while True:
        sock_conn, client_addr = sock_listen.accept()
        client_socks.append((sock_conn, client_addr))
        # threading.Thread(target=client_chat, args=(sock_conn, client_addr)).start()
        threading.Thread(target=user_service_thread,args=(sock_conn,client_addr)).start()


if __name__ == "__main__":
    main()

