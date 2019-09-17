#!usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading 
import tkinter as tk
import tkinter.messagebox
import json



def index_page():
    '''
    函数内容：聊天登录注册主页面
    '''
    global reg_uname
    global reg_passwd

    mainwdn = tk.Tk()
    mainwdn = title("welcome to Jayne'home")
    mainwdn.minsize(400,300) 
    mainwdn.resizable(0,0)
    
    photo=tkinter.PhotoImage(file=r"C:\Users\lx\Documents\Visual Studio Code\聊天室\img\1.gif")
    # photo=tkinter.PhotoImage(file=r"C:\Users\lx\Documents\Visual Studio Code\聊天室\img\plent.jpg")
    label=tkinter.Label(mainwdn,image=photo)  #图片
    label.pack()
    
    tk.Label(mainwdn, text='账号：', font=('Arial', 14)).place(x=100, y=150)
    tk.Label(mainwdn, text='密码：', font=('Arial', 14)).place(x=100, y=200)
    
    reg_uname = tk.Entry(mainwdn, show=None, font=('Arial', 12))     # 输入账号信息的Entry控件
    reg_uname.place(x=250, y=150)
    reg_passwd = tk.Entry(mainwdn, show='*', font=('Arial', 12))      # 输入密码信息的Entry控件
    reg_passwd.place(x=250, y=200)
    
    tk.Button(mainwdn, text='登录', font=('Arial', 14), command=client_login_send).place(x=190, y=320)
    tk.Button(mainwdn, text='注册', font=('Arial', 14), command=login_in).place(x=320, y=320)

def chat_window():
    '''
    函数内容：聊天窗口
    '''
    global chat_msg_box
    global chat_record_box

    mainwdn = tk.Tk()
    mainwdn = title("P1901班专属聊天室")
    

    # 设置聊天框
    chat_record_box = tk.Text(mainwdn)
    chat_record_box.configure(state=tk.DISABLED)
    chat_record_box.pack(padx=10, pady=10)
    
    # 设置输入框
    chat_msg_box = tk.Text(mainwdn)
    chat_msg_box.configure(width=65, height=5)
    chat_msg_box.pack(side=tk.LEFT, padx=10, pady=10)
    

    send_msg_btn = tk.Button(mainwdn, text="发 送", command=on_send_msg)
    send_msg_btn.pack(side=tk.RIGHT, padx=10, pady=10, ipadx=15, ipady=15)
    
    threading.Thread(target=recv_chat_msg).start()
    
    mainwdn.mainloop()     # 主窗口循环显示

def login_in():
    '''
    函数内容：用户注册页面
    '''
    global log_uname
    global log_passwd
    global log_phone
    global log_email

    mainwdn = tk.Tk()
    mainwdn.title('chat-login')
    mainwdn.minsize(400,300)
    mainwdn.resizable(0,0)
    
    tk.Label(mainwdn_log, text='账号：', font=('Arial', 14)).place(x=25, y=60)
    tk.Label(mainwdn_log, text='密码：', font=('Arial', 14)).place(x=25, y=90)
    tk.Label(mainwdn_log, text='确认密码：', font=('Arial', 14)).place(x=25, y=120)
    tk.Label(mainwdn_log, text='手机号：', font=('Arial', 14)).place(x=25, y=150)
    tk.Label(mainwdn_log, text='邮箱：', font=('Arial', 14)).place(x=25, y=180)
    log_uname = tk.Entry(mainwdn_log, show=None, font=('Arial', 12))   # 输入注册账号信息的Entry控件
    log_uname.place(x=150, y=60)
    log_passwd = tk.Entry(mainwdn_log, show=None, font=('Arial', 12))   # 输入注册密码信息的Entry控件
    log_passwd.place(x=150, y=90)
    log_np = tk.Entry(mainwdn_log, show=None, font=('Arial', 12))  # 第二次输入注册密码信息的Entry控件
    log_np.place(x=150, y=120)
    log_phone = tk.Entry(mainwdn_log, show=None, font=('Arial', 12))   # 输入注册手机号信息的Entry控件
    log_phone.place(x=150, y=150)
    log_email = tk.Entry(mainwdn_log, show=None, font=('Arial', 12))   # 输入注册邮箱信息的Entry控件
    log_email.place(x=150, y=180)
    
    tk.Button(mainwdn_log, text='注册', font=('Arial', 14), command=client_login_send).place(x=180, y=220)
    
    mainwdn.mainloop()


def client_login_send():
    '''
    函数功能：用户登录请求
    '''
    myuname = reg_uname.get()
    mypasswd = reg_passwd.get()
    req = {"op": 1, "args":{"uname": myuname, "passwd": mypasswd}}
    req = json.dumps(req)
    data_top="{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())
    client_login_recv()


def client_login_recv():
    '''
    函数功能：用户登录响应
    '''
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
    
        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            # print("登录成功！")
            index_page()


def client_reg_send():
    '''
    函数功能：用户注册请求
    '''
    myuname = log_uname.get()
    mypasswd = log_passwd.get()
    myphone = log_phone.get()
    myemail = log_email.get()
    req = {"op": 2, "args": {"uname": myuname, "passwd": mypasswd, "phone": myphone, "email": myemail}}
    req = json.dumps(req).encode()
    data_top = "{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req)
    client_reg_recv()


def reg_success_page():
    '''
    函数内容：注册成功界面
    '''
    # 创建tk对象
    mainwdn = tk.Tk()

    # 设置窗口标题
    mainwdn.title("注册成功！")
    
    # 设置窗口大小
    mainwdn.minsize(400, 300)
    
    # 设置窗口能否变长变宽，默认为True
    mainwdn.resizable(0,0)
    
    # 设置用户名标签
    tk.Label(mainwdn, text="恭喜注册成功!!!", font=("Arial", 18)).place(x = 110, y = 120)
    
    tk.Button(mainwdn, text="返回登录界面", font=("Arial", 12), command=index_page).place(x = 270, y = 250)
    
    mainwdn.mainloop()

def reg_failed_page():
    '''
    函数内容：注册失败界面
    '''
    # 创建tk对象
    mainwdn = tk.Tk()

    # 设置窗口标题
    mainwdn.title("注册失败！")
    
    # 设置窗口大小
    mainwdn.minsize(400, 300)
    
    # 设置窗口能否变长变宽，默认为True
    mainwdn.resizable(0,0)
    
    # 设置用户名标签
    tk.Label(mainwdn, text="注册失败!!!", font=("Arial", 18)).place(x = 110, y = 120)
    
    tk.Button(mainwdn, text="返回注册界面", font=("Arial", 12), command=login_in).place(x = 270, y = 250)
    
    mainwdn.mainloop()


def client_reg_recv():
    '''
    函数功能：用户注册响应
    '''
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
    
        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            reg_success_page()
        else:
            # print("注册失败！")
            reg_failed_page()


def on_send_msg():
    '''
    函数功能：发送聊天消息
    '''
    nick_name = reg_uname.get()
    chat_msg = chat_msg_box.get(1.0)
    if chat_msg == "\n":
        return 

    chat_data = nick_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()
    try:
        sock.send(data_len + chat_data)
    except:
        messagebox.showerror("温馨提示", "发送消息失败，请检查网络连接！")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=DISABLED)

def recv_chat_data():
    '''
    函数功能：接收聊天消息
    '''
    global sock

    while True:
        try:
            while True:
                msg_len_data = sock.recv(15)
                if not msg_len_data:
                    break
    
                msg_len = int(msg_len_data.decode().rstrip())
                recv_size = 0
                msg_content_data = b""
                while recv_size < msg_len:
                    tmp_data = sock.recv(msg_len - recv_size)
                    if not tmp_data:
                        break
                    msg_content_data += tmp_data
                    recv_size += len(tmp_data)
                else:
                    # 显示
                    chat_record_box.configure(state=NORMAL)
                    chat_record_box.insert(msg_content_data.decode() + "\n")
                    chat_record_box.configure(state=DISABLED)
                    continue
                break
        finally:
                sock.close()
                sock = socket.socket()
                sock.connect(("192.168.10.171", 9999))

sock = socket.socket()
sock.connect(("192.168.10.171", 9999))

if __name__ == "__main__":
    index_page()

