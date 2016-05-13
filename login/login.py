#/usr/bin/env python
#-*- coding:utf-8 -*-
#Authot:Zhang Yan

import sys,time,os,re
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText

confg_file = "userauth.txt"            #定义配置文件(存放邮箱信息,admin和普通用户的信息)
if not os.path.exists(confg_file):      #如果配置文件不存在
    sys.exit("不能找到用户配置文件 %s" % confg_file)  #退出系统
cf = ConfigParser()                     #构造一个configparse对象用来读取配置文件
cf.read(confg_file)                     #读取配置文件
userlist=eval(cf.get("admin","userlist"))  #从配置文件中取用户列表
blacklist=eval(cf.get("admin","blacklist")) #从配置文件中取黑名单列表

mailto_list=[cf.get("mail","mail_to")]     #从配置文件取收件人
mail_host=cf.get("mail","mail_host")  #设置邮件服务器,从配置文件中取
mail_user=cf.get("mail","mail_user")    #从配置文件中取发件人用户名
mail_pass=cf.get("mail","mail_pass")   #从配置文件中取发件人客户端授权密码
mail_postfix=cf.get("mail","mail_postfix")  #从配置文件中取发件箱的后缀

def send_mail(sub,content,to_list=mailto_list):     #发送邮件函数
    me="本地部署"+"<"+mail_user.split('@')[0]+"@"+mail_postfix+">"   #定义发件人
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')       #发送信息
    msg['Subject'] = sub                                            #发送主题
    msg['From'] = me                                                #邮件抬头
    msg['To'] = ";".join(to_list)                                   #邮件抬头
    try:                                                            #try方法
        server = smtplib.SMTP()                                     #构造邮件对象
        server.connect(mail_host)                                   #连接邮件服务器
        server.login(mail_user,mail_pass)                           #登录邮箱
        server.sendmail(me, to_list, msg.as_string())               #发送邮件
        server.close()                                              #关闭邮箱
        return True                                                 #发送成功返回True
    except Exception as e:
        print(str(e))
        return False                                                #失败返回False

def mail_check():
    while True:
        mailto=input("请输入您可以接收邮件的邮箱:")      #输入接收邮件的邮箱
        if mailto == "":                            #输入不能为空
            print("必须设置接收邮件的邮箱!")
        elif len(mailto) > 7 and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", mailto) != None: #正则检查邮箱输入格式是否正确
            cf.set("mail", "mail_to", mailto)  #正确的话,将邮箱写入配置文件
            cf.write(open("userauth.txt", "w"))
            break           #退出循环
        else:               #不正确重新输入
            print("您输入的邮箱格式有误!请重新输入!")

def show(show_flag,name):                        #显示函数
    if show_flag == "1":                         #如果显示选项是"1",打印下面的内容
        print('''
            #################################
                       欢迎光临商城!
                    登录       管理员登录
            #################################
            ''')
    elif show_flag == "2":                      #如果显示选项是"2",打印下面的内容
        print('''
            ################################
                     欢迎光临商城!
                                 %s
             您可以进行以下操作:
             (1) 注销
             (2) 修改密码
             (3) 退出系统
            ################################
        ''' % name)
    else:                                       #如果显示选项是"3",打印下面的内容
        print('''
            ################################
             管理员:%s恭喜您登录成功!
             您可以进行以下操作:
             (1) 注销
             (2) 修改密码
             (3) 用户解锁
             (4) 退出系统
            ################################
        ''' % name)

def login():                                #登录函数
    locked = {}                             #定义字典locked来存放每个用户的允许失败登录次数
    for na in userlist:                     #每个用户登录失败3次就被锁定
        locked[na] = 3
    show("1","aa")                          #打印提示登录页面
    while True:
        name=input("请输入您的登录用户名:")     #登录的用户名
        passwd=input("请输入您的登录密码:")     #登录的密码
        if name == "admin":                 #如果是管理员登录
            print("您好,您正在用管理员账号登录,请确保您是管理员!")
            print("注意:管理员只有一次登录机会且只能通过邮件解锁!")
            if passwd == cf.get("admin","password"):  #从配置文件里取管理员的密码和输入密码比较
                show("3",name)              #如果相同则登录成功,打印管理员的登录信息
                user(name)                  #调用user()函数进行之后的操作(改密码,解锁等等)
            else:                           #如果登录不成功
                st=input("管理员已锁定!是否发送解锁邮件? y/n")  #选择是否联系管理员解锁
                if st.lower() == "y":                   #选是
                    if send_mail("解锁邮件", "用户%s申请解锁!\n请点击下面的链接进行解锁:http://jiesu.com" % name):    #给管理员发送邮件
                        print("管理员解锁函数待开发.......")  #因为管理员不能给管理员解锁,所以打算通过类似一般网站的重置密码方式进行解锁,所以先空着
                else:   #如果选择不发邮件,因为是管理员登录,所以直接强制退出系统
                    sys.exit("管理员已被锁定,强制退出系统!")
        elif name in userlist:        #如果是普通用户登录,判断用户是不是在用户列表里,如果在
            if name in blacklist:     #判断用户是不是在黑名单列表里,如果在,说明用户之前输入密码错误3次已经被锁定啦
                st=input("%s 用户已被锁定!请问是否联系管理员找回密码? y/n" % name)  #是否联系管理员解锁
                if st.lower() == "y":   #选是
                    send_mail("解锁邮件","用户%s申请解锁!" % name)  #给管理员发送邮件
                else:                   #选否
                    st = input("是否切换用户? y/n")               #是否切换用户
                    if st.lower() == "y":                       #选是
                        continue                                #继续循环
                    else:                                       #选否
                        print("此用户将被锁定5秒!请稍后再试")       #用户被锁定5秒后自动解锁(实际情况中这个时间拉长)
                        for i in range(5):                      #锁定5秒
                            print("wait.." * (i + 1))
                            time.sleep(1)
                        blacklist.remove(name)                  #用户从黑名单里移除,解锁
                        cf.set("admin", "blacklist", str(blacklist))    #将修改后的黑名单写入配置文件
                        cf.write(open("userauth.txt", "w"))
                        continue                                #继续循环
            else:                                               #如果用户不在黑名单里
                if passwd == cf.get(name,"password"):           #从配置文件获取用户的密码,如果输入密码与文件中的密码匹配
                    show("2",name)                              #打印普通用户登录成功信息
                    user(name)                                  #调用user函数,执行之后的操作(改密码等等)
                else:                                           #如果密码不匹配
                    locked[name]-=1                             #用户允许失败登录次数减1
                    if locked[name] == 0:                       #如果用户允许登录失败次数变为0
                        print("您已三次输入密码不正确!%s 用户已被锁定!" % name)           #则输出三次登录失败信息
                        blacklist.append(name)                  #加入黑名单
                        cf.set("admin","blacklist",str(blacklist))
                        cf.write(open("userauth.txt","w"))
                    else:                                       #如果用户允许登录次数不为0
                        print("您输入的密码不正确!您还有%d次机会!请重新输入!" % locked[name]) #提示密码输入失败,重新输入
                        continue
        else:                       #如果输入name既不是admin又不是普通用户,输出用户未注册,重新输入
            print("未在库中找到您的用户名%s,请确认您已注册并且输入用户名正确!" % name)
            continue

def user(name):                 #user函数
    while True:
        if name == "admin":     #如果登录的用户是admin,可输入选项为下:
            st1 = input("请输入您要进行的操作:A 注销 B 修改密码 C 退出系统 D 用户解锁")
        else:                   #如果登录的是普通用户,可输入选项为下:
            st1=input("请输入您要进行的操作:A 注销 B 修改密码 C 退出系统")
        if st1.upper() == "A":  #如果输入为A,注销账号
            print("您已成功注销,3秒后自动跳入首页!")
            for j in range(3):   #等待3秒跳到首页
                print("#"*(j+1))
                time.sleep(1)
            login()             #调用登录函数,重新开始登录
        elif st1.upper() == "B":    #如果输入为B,改密码
            pass_old=input("请输入旧密码:") #先输入旧密码
            if pass_old == cf.get(name,"password"):  #判断旧密码是不是和文件中保存的一致,如果一致
                for k in range(3):                   #有三次输入新密码的机会
                    pass_new=input("请输入您的新密码:") #输入新密码
                    pass_new2=input("请再次输入您的新密码:") #确认新密码
                    if pass_new == pass_new2:           #如果两次输入新密码一致
                        cf.set(name,"password",pass_new)    #将新密码更新进配置文件
                        cf.write(open("userauth.txt", "w"))
                        print("恭喜您修改密码成功!Y(^_^)Y")
                        break
                    else:                           #如果两次新密码输入不一致
                        if k == 2:                  #如果三次机会都用完
                            print("您已三次输入错误!我已严重怀疑您的智商→_→ ")
                        else:                       #否则重新输入新密码
                            continue
            else:                               #如果旧密码输入错误
                print("很抱歉,您的旧密码输入有误,您无法修改密码!")
        elif st1.upper() == "C":        #如果输入为C
            sys.exit("欢迎您的下次光临!=^_^=")
        elif st1.upper() == "D":        #如果输入为D,分两种情况
            if name == "admin":         #如果是admin用户输入为D,就是要解锁普通用户
                username=input("请输入您要解锁的用户:")   #输入要解锁的用户
                if username in blacklist:               #如果要解锁的用户在黑名单里
                    blacklist.remove(username)          #解锁
                    cf.set("admin","blacklist",str(blacklist))
                    cf.write(open("userauth.txt","w"))
                    print("用户%s解锁成功!" % username)
                else:                                   #否则提示输入有误
                    print("您的输入有误!您输入的用户%s不在黑名单里!" % username)
            else:
                print("您输入的有误,请重新输入!")  #如果普通用户输入D,则提示输入有误
        else:                                   #输入别的都是输入有误
            print("您输入的有误,请重新输入!")

if __name__ == "__main__":
    mail_check()
    login()  #调用login函数开始登录

