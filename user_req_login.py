#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import re
import urllib.parse
import urllib.request
import json
import random
import sys


def check_user_name(user_name):
    '''
    函数功能：校验用户是否合法
    函数参数：
    user_name 待校验的用户
    返回值:校验通过返回0，校验失败返回非0(格式错误返回1，用户名已存在返回2)
    '''

    ## 校验所输格式是否符合规范
    ## [0-9a-zA-Z_]{6,15}  匹配任意的数字、字母和下划线
    if not re.match("^[0-9a-zA-Z_]{6,15}$",user_name):
        return 1      # 格式错误返回1

    ## 连接数据库,conn为Connection对象
    conn = pymysql.connect("192.168.8.108","dj","123456","mdb")

    try:
    ## 获取一个游标对象，用于执行SQL语句
        with conn.cursor() as cur:
            cur.execute("select uname from user where uname=%s",(user_name,))
            rows = cur.fetchone()
    finally:
    
        ## 关闭数据库的连接
        conn.close()
    if rows:      # 判断字符串是否为空集
        return 2

    return 0      # 符合规范返回0


    # for t in rows:
    #     if user_name in t:
    #         return 2      # return 2 : 重复的话,返回2


           
def check_password(password):
    '''
    函数功能：校验用户密码是否合法
    函数参数：
    password 待校验的密码
    返回值:校验通过返回0，校验失败返回非0(密码太长会太短返回1，密码安全强度太低返回2)
    '''
    
    return 0
   
   
def check_uname_pwd(user_name,password):
    '''
    函数功能：校验用户和密码是否合法
    函数参数：
    user_name 待校验的用户
    password  待校验的密码
    返回值:校验通过返回0，校验失败返回1
    '''
    
    ## 连接数据库,conn为Connection对象
    conn = pymysql.connect("192.168.8.108","dj","123456","mdb")

    try:
    ## 获取一个游标对象，用于执行SQL语句
        with conn.cursor() as cur:
            cur.execute("select uname from user where uname=%s and passwd=password(%s)",(user_name,password))
            rows = cur.fetchone()
    finally:
    
        ## 关闭数据库的连接
        conn.close()
    if rows:      
        return 0

    return 1    



def check_phone(phone):
    '''
    函数功能：校验手机号是否合法
    函数参数：
    phone 待校验的手机号
    返回值:校验通过返回0，校验错误返回1
    '''
    if not re.match("^1[35678]\d(10)$",phone):
        return 0

    return 1

# def check_email(email):
#     if re.match(r"^[0-9a-zA-Z_]{0,19}@qq.com$",email):
#         break
#     else:
#         print("邮箱格式有误,请重新输入:")



def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''

    verify_code = str(random.randint(100000,999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile" : phone, #接收短信的手机号码
            "tpl_id" : "162901", #短信模板ID，请参考个人中心短信模板设置
            "tpl_value" : "#code#=%s" % verify_code, #变量名和变量值对。如果你的变量名或者变量值中带有#&amp;=中的任意一个特殊符号，请先分别进行urlencode编码后再传递，&lt;a href=&quot;http://www.juhe.cn/news/index/id/50&quot; target=&quot;_blank&quot;&gt;详细说明&gt;&lt;/a&gt;
            "key" : "您申请的是appkey", #应用APPKEY(应用详细页查询)     
        }

        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)

        if res and res['error_code'] == 0:
            return verify_code
        else:
            return False
    except:
        return False

def send_email_code(email):
    '''
    函数功能：发送邮箱验证码（6位随机数）
    函数参数：
    email 接收验证码的邮箱
    返回值：发送成功返回验证码，失败返回False
    '''

    verify_code = str(random.ranodint(100000,999999))

    return verify_code


def user_reg(uname,password,phone,email):
    '''
    函数功能：将用户注册信息写入数据库
    函数描述：
    uname 用户名
    password 密码
    phone 手机号
    email 邮箱
    返回值：成功返回True，失败返回False
    '''

    conn = pymysql.connect("127.0.0.1","fxj","123456","test")

    try:
    ## 获取一个游标对象，用于执行SQL语句
        with conn.cursor() as cur:
            cur.execute("insert into user (uname,passwd,phone,email) values (%s,password(%s),%s,%s",(uname,passwd,phone,email))
            r = cur.fetchcount
            conn.commit()
    finally:

        ## 关闭数据库的连接
        conn.close()

    return bool(r)
    



def reg_main():
    while True:
        user_name = input("请输入用户名(只能包含英文字母,数字或下划线,最短6位,最长15位):")

        ret = check_user_name(user_name)

        if ret == 0:
            break
        elif ret == 1:
            print("用户名格式错误,请重新输入!")
        elif ret == 2:
            print("用户名已存在,请重新输入!")
            
    while True:
        while True:
            password = input("请输入密码:")

            ret = check_password(password)

            if ret == 0:
                break
            elif ret == 1:
                print("密码不符合长度要求,请重新输入!")
            elif ret == 2:
                print("密码太简单,请重新输入!")

        confirm_pass = input("请再次输入密码:")

        if password == confirm_pass:
            break
        else:
            print("两次输入的密码不一致，请重新输入!")


    while True:
        phone = input("请输入手机号：")

        if check_phone(phone):
            print("手机号输入错误，请重新输入！")
        else:
            break


    verify_code = send_sms_code(phone)
    
    if verify_code:
        print("短信验证码已发送！")
    else:
        print("短信验证码发送失败，请检查网络连接或联系软件开发商！")
        sys.exit(1)

    while True:
        verify_code2 = input("请输入短信验证码：")

        if verify_code2 != verify_code:
            print("短信验证码输入错误,请重新输入！")
        else:
            break
        
    email = input("请输入邮箱：")

    if user_reg(user_name,password,phone,email):
        print("注册成功！")
    else:
        print("注册失败")




def login_main():
    '''
    函数功能：用户登录验证
    函数参数：无
    返回值：登录验证成功返回用户名，失败返回False
    '''

    while True:
        user_name = input("\n用户名:")
        ret = check_user_name(user_name)   
        if ret == 0:
            print("用户名不存在,请重新输入！")
        elif ret == 1:
            print("用户名格式错误,请重新输入！")
        else:
            break

    while True:
        password = input("\n密码:")
        ret = check_password(password)
        if ret == 0:
            break
        else:
            print("密码格式错误,请重新输入！")
        
    if check_uname_pwd(user_name,password):
        return False
    return user_name



def user_center(user_name):
    print("%s,欢迎你使用本系统!" % user_name)
    print("\n操作提示：")
    print("1：盘点库存")
    print("2：查看销售额")
    print("3：修改个人密码")
    print("0：退出")  

    while True:
        op = input("\n>: ")

        if op == "0":
            print("感谢你的使用，下次再见！")
            sys.exit(2)
        elif op == "1":
            print("程序员正在紧急写程序，敬请关注！")    
        elif op == "2":
            print("程序员正在紧急写程序，敬请关注！")
        elif op == "3":
            print("程序员正在紧急写程序，敬请关注！")        
        else:
            print("输入错误，请重新输入！")  




def main():
    print("操作提示：")
    print("1：登录")
    print("2：注册")
    print("0：退出")

    while True:
        op = input("\n>: ")

        if op == "0":
            print("感谢你的使用，下次再见！")
            sys.exit(2)
        elif op == "1":
            user_name = login_main()
            if user_name:
                # print("登陆成功！")
                user_center(user_name)
            else:
                print("密码错误，登陆失败！")
        elif op == "2":
            reg_main()
        else:
            print("输入错误，请重新输入！")
    
 
if __name__ == '__main__':
    main()