import tkinter as tk
import tkinter.messagebox
import pickle
# from PIL import ImageTk, Image
import pymysql
import time
import threading
import socket


window = tk.Tk()                               # 创建根窗口
window.title("P1901班专属聊天室")
window.geometry('500x400')


# canvas = tk.Canvas(window, width=1200,height=699,bd=0, highlightthickness=0)
# imgpath = '1.gif'
# img = Image.open(imgpath)
# photo = ImageTk.PhotoImage(img)

# canvas.create_image(700, 500, image=photo)
# canvas.pack()
# entry=tk.Entry(window,insertbackground='blue', highlightthickness =2)
# entry.pack()

# canvas.create_window(100, 50, width=100, height=20,window=entry)

photo=tkinter.PhotoImage(file=r"C:\Users\lx\Documents\Visual Studio Code\tkinter\1.gif")
label=tkinter.Label(window,image=photo)  #图片
label.pack()


# 在根窗口上放置相应标签和Entry控件，并摆放好位置
tk.Label(window, text='欢迎!', font=('Arial', 20)).pack()
tk.Label(window, text='通行证账号：', font=('Arial', 14)).place(x=50, y=100)
tk.Label(window, text='密码：', font=('Arial', 14)).place(x=50, y=150)
e_u = tk.Entry(window, show=None, font=('Arial', 12))     # 输入账号信息的Entry控件
e_u.place(x=200, y=105)
e_p = tk.Entry(window, show='*', font=('Arial', 12))      # 输入密码信息的Entry控件
e_p.place(x=200, y=155)


# fr = open(r"C:\\Users\lx\Documents\Visual Studio Code\tkinter\userdate.txt", 'rb')         # 以二进制方式打开一个文件（只读）
# user_info = pickle.load(fr)             # 使用load()将数据从文件中序列化读出
# fr.close()                              # 关闭文件


def on_send_msg():
    nick_name = "Jayne"
    chat_msg = chat_msg_box.get(1.0, "end")
    if chat_msg == "\n":
        return

    chat_data = nick_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()
    
    try:
        sock.send(data_len)
        sock.send(chat_data)
    except:
        # sock.close()
        tk.messagebox.showerror("温馨提示", "发送消息失败，请检查网络连接！")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=tk.NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=tk.DISABLED)


def recv_chat_msg():
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
                        chat_record_box.configure(state=tk.NORMAL)
                        chat_record_box.insert("end", msg_content_data.decode() + "\n")
                        chat_record_box.configure(state=tk.DISABLED)
                        continue
                    break
        finally:
                sock.close()
                sock = socket.socket()
                sock.connect(("0.0.0.1", 9999))

sock = socket.socket()
sock.connect(("0.0.0.1", 9999))

def update_show_time(show_text):
    datetime = time.localtime()
    show_text.set("%s-%s-%s %s:%s:%s 星期%s" % (datetime[:6] + (weekday[datetime[6]], )))

    t = threading.Timer(1, update_show_time, (show_text, ))
    t.start()
    
    weekday = ("一", "二", "三", "四", "五", "六", "日")
    show_text = tk.StringVar()
    datetime = time.localtime()
    show_text.set("%s-%s-%s %s:%s:%s 星期%s" % (datetime[:6] + (weekday[datetime[6]], )))
    lblTime = tk.Label(window, textvariable=show_text)
    lblTime.pack()
    
    t = threading.Timer(1, update_show_time, (show_text, ))
    t.start()



# 登录函数
def sign_in():
    try:
        with open(r'C:\Users\lx\Documents\Visual Studio Code\tkinter\userdate.txt','rb') as fr:
            user_info = pickle.load(fr)
            return user_info
    except EOFError: #捕获异常EOFError 后返回None
        return None



    # 通行证账号判断
    flag = 1                 # 设定标志位（标志：输入通行证账号不能为空）
    if e_u.get() == '':      # 判断用户是否输入通行证账号
        flag = 0
        tkinter.messagebox.showerror(title='抱歉！', message='输入通行证账号不能为空！')
    
    i = 0
    flag_1 = 0               # 设定标志位（标志：是否从用户信息中遍历到用户所输入的通行证账号）
    for key in user_info:    # 遍历用户信息
        if (key == e_u.get()) & (flag == 1):     # 若用户已经输入账号且从用户信息中遍历到账号
            flag_1 = 1
            user_p = user_info[key]              # 将用户信息的账号所对应的密码提取出来
            break
        i += 1
        if (i == len(user_info)) & (flag == 1):  # 若遍历结束后没有发现用户所输入账号，则输出通行证账号不存在
            tkinter.messagebox.showerror(title='抱歉！', message='通行证账号不存在')
    
    # 密码判断
    if flag_1 == 1:                              # 标志位判断（成立：已经遍历到账号信息，不成立：没有遍历到账号信息）
        if e_p.get() == '':                      # 判断用户所输入密码是否为空
            tkinter.messagebox.showerror(title='抱歉！', message='输入密码不能为空！')
    
        elif user_p == e_p.get():                # 判断用户所输入密码与从用户信息文件中取出的密码是否相同
            tkinter.messagebox.showinfo(title='恭喜您！', message='登陆成功！')
            window.quit()                        # 登陆成功，关闭根窗口
        else:
            tkinter.messagebox.showwarning(title='抱歉', message='密码有误，请重新输入！')

def connect_sql():
    conn = pymysql.connect(("localhost", "fxj", "123456", "test"))
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # SQL 插入语句
    sql = "INSERT INTO user(name, pwd) VALUES ('%s', '%s')" % (e_u,e_p)
    try:
        # 执行sql语句
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        print("数据插入成功！！！")
        # 提交到数据库执行
        conn.commit()
    except:
        print("数据插入失败！！！")
        # Rollback in case there is any error
        conn.rollback()

    # 关闭游标
    cursor.close()
    # 关闭数据库的连接
    conn.close()


# 注册函数
def b_register():
    def register():
        # 通行证账号检测
        flag_2 = 1                               # 设定标志位（标志：用户输入的通行证账号是否为空）
        if e_register_u.get() == '':             # 判断用户输入的通行证账号是否为空
            flag_2 = 0
            tkinter.messagebox.showerror(title='抱歉！', message='输入通行证账号不能为空！')

        flag_3 = 1                               # 设定标志位（标志：用户输入的通行证账号是否已被注册）
        for key in user_info:                    # 遍历用户信息
            if (key == e_register_u.get()) & (flag_2 == 1):    # 若用户输入的通行证账号不为空，且遍历到的账号信息与输入的相同
                flag_3 = 0
                tkinter.messagebox.showerror(title='抱歉！', message='该通行证账号已注册！')
    
        #密码检测
        flag_4 = 1                               # 设定标志位（标志：用户输入密码是否为空）
        if (e_register_p.get() == '') & (flag_2 == 1):     # 若用户输入的通行证账号不为空，且输入的密码为空
            flag_4 = 0
            tkinter.messagebox.showerror(title='抱歉！', message='输入密码不能为空！')
    
        if (e_register_p.get() != e_register_np.get()) & (flag_3 == 1):        #判断两次密码输入是否一致
            tkinter.messagebox.showwarning(title='抱歉', message='两次密码输入不一致，请重新输入！')
    
        # 两次密码输入一致，进行下面操作
        if (e_register_p.get() == e_register_np.get()) & (flag_2 == 1) & (flag_3 == 1) & (flag_4 == 1):
            user_info[e_register_u.get()] = e_register_p.get()       # 将输入的账号、密码存储在字典中
    
            with open(r"C:\\Users\lx\Documents\Visual Studio Code\tkinter\userdate.txt", 'wb') as fw:   # 以二进制方式打开一个文件（只写）
                pickle.dump(user_info, fw)                               # 使用dump()将数据序列化到文件中
                fw.close()                                               # 关闭文件
    
            tkinter.messagebox.showinfo(title='恭喜您！', message='注册成功！')
            window_register.destroy()                               # 关闭注册窗口


    window_register = tk.Toplevel(window)                            # 在根窗口上建立一个注册窗口
    window_register.title('Register Window')
    window_register.geometry('400x300')
    
    window_register = connect_sql()


    # 在注册窗口上放置相应标签和Entry控件，并摆放好位置
    tk.Label(window_register, text='通行证账号：', font=('Arial', 14)).place(x=25, y=50)
    tk.Label(window_register, text='密码：', font=('Arial', 14)).place(x=25, y=100)
    tk.Label(window_register, text='确认密码：', font=('Arial', 14)).place(x=25, y=160)
    e_register_u = tk.Entry(window_register, show=None, font=('Arial', 12))   # 输入注册账号信息的Entry控件
    e_register_u.place(x=165, y=50)
    e_register_p = tk.Entry(window_register, show=None, font=('Arial', 12))   # 输入注册密码信息的Entry控件
    e_register_p.place(x=165, y=100)
    e_register_np = tk.Entry(window_register, show=None, font=('Arial', 12))  # 第二次输入注册密码信息的Entry控件
    e_register_np.place(x=165, y=160)
    # 在注册窗口上建立一个按键
    b_sign_in_register = tk.Button(window_register, text='确认注册', font=('Arial', 14), command=register).place(x=180, y=220)

# 在根窗口上建立两个按键
b_sign_in = tk.Button(window, text='登录', font=('Arial', 14), command=sign_in).place(x=190, y=220)
b_register = tk.Button(window, text='注册', font=('Arial', 14), command=b_register).place(x=320, y=220)


chat_record_box = tk.Text(window)
chat_record_box.configure(state=tk.DISABLED)
chat_record_box.pack(padx=10, pady=10)

chat_msg_box = tk.Text(window)
chat_msg_box.configure(width=65, height=5)
chat_msg_box.pack(side=tk.LEFT, padx=10, pady=10)

send_msg_btn = tk.Button(window, text="发 送", command=on_send_msg)
send_msg_btn.pack(side=tk.RIGHT, padx=10, pady=10, ipadx=15, ipady=15)

threading.Thread(target=recv_chat_msg).start()

window.mainloop()     # 主窗口循环显示

sock.close()