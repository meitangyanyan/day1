#/usr/bin/env python
#-*- coding:utf-8 -*-
#Authot:Zhang Yan
from configparser import ConfigParser
import os,sys,datetime
from login import mail_check,login

db = "db.txt"            #定义配置文件(存放邮箱信息,admin和普通用户的信息,以及商品库存信息)
if not os.path.exists(db):      #如果配置文件不存在
    sys.exit("不能找到用户配置文件 %s" % db)  #退出系统
cf = ConfigParser()                     #构造一个configparse对象用来读取配置文件
cf.read(db,encoding="utf8")                     #读取配置文件

goods={
    "服装":{
        "女装":[("连衣裙",100),("女裤",80),("女牛仔裤",50),("女T恤",90),("女鞋",50)],
        "男装":[("男裤",80),("男牛仔裤",50),("男T恤",90),("男鞋",50)]
    },
    "通信":{
        "手机":[("华为手机",3000),("Iphone",6000),("小米手机",1000)],
        "电脑":[("联想电脑",6000),("华硕电脑",4000),("mac",12000)]
    }
}
#将字典类型的参数转化成列表并返回的函数(将字典goods的每一层都转换成一个列表,实现三级菜单)
def show(name,flag):
    menu=[]
    print("商品列表如下:")
    if flag == 0:
        print("编号".ljust(10), "商品")
        for k, j in enumerate(name):
            menu.append(j)
            print(str(k).ljust(12), j)
    if flag == 1:
        print("编号", "商品".center(20),"价格")
        for k, j in enumerate(name):
            menu.append(j)
            print(k, j[0].center(30),j[1])
    return menu
#商品展示(三级菜单函数)
def show_goods():
    print("欢迎光临本商城".center(50, "-"))
    while True:
        menu1 = show(goods,0)
        num1=input("\033[37;1m请问您想查看哪类商品呢?请输入对应的编号:\033[0m")
        if num1.isdigit() and int(num1) < len(menu1):
            goods1=goods[menu1[int(num1)]]
            menu2=show(goods1,0)
            while True:
                num2=input("\033[33;1m(b or back返回上一级)\033[0m\033[37;1m请问您想查看哪类商品呢?请输入对应的编号:\033[0m")
                if num2.isdigit() and int(num2) < len(menu1):
                    goods2=goods1[menu2[int(num2)]]
                    menu3 = show(goods2,1)
                    return menu3
                elif num2 == "b" or num2 == "back":
                    break
                else:
                    print("您的输入有误！请重新输入！")
                    continue
        else:
            print("您的输入有误！请重新输入！")
            continue
#购物函数(此购物函数可以选择立即下单和加入购物车两种模式,立即下单会立即结算,购买的商品信息会保存到db.txt文件的对应用户的order变量里,购物车商品信息会保存到cart变量里)
#(此购物函数允许用户一次购买多个商品,还可以判断商品的库存是否充足,商品的库存保存在db.txt文件的"库存"的对应商品名的变量里)
def shop_func(user):
    balance=int(cf.get(user,"salary"))
    cart=eval(cf.get(user,"cart"))
    order=eval(cf.get(user,"order"))
    exit_flag=False
    goods_list = show_goods()
    while not exit_flag:
        kind=input("\033[31;1m您想查看别的分类的商品吗？y/n\033[0m")
        if kind == "y":
            goods_list = show_goods()
            continue
        elif kind == "n":
            pass
        else:
            print("您输入的有误，请重新输入！")
            continue
        num = input("\033[33;1m(q as quit)\033[0m\033[37;1m请输入您想购买的商品的编号:\033[0m")
        if num == "q" or num == "quit":
            print("您购买的商品有:")
            for index, items in enumerate(order):
                print("[%d] 商品[%s]  数量[%d]" % (index,items[0], items[1]))
            print("您的购物车未结算商品有：")
            for index, items in enumerate(cart):
                print("商品[%s]  数量[%d]" % (items[0], items[1]))
            print("您的余额为\033[31;1m[%d]\033[0m" % balance)
            cf.set(user,"salary",str(balance))
            cf.set(user,"cart",str(cart))
            cf.set(user,"order",str(order))
            cf.set("库存",p_name,str(p_stock))
            cf.write(open(db,"w"))
            exit_flag = True
        elif num.isdigit() and int(num) < len(goods_list):
            num = int(num)
            p_name = goods_list[num][0]
            p_price = goods_list[num][1]
            p_stock = int(cf.get("库存", p_name))
            print("您要购买的商品的库存是[%d]" % p_stock)
            buy_num = input("\033[37;1m请输入您要购买的商品的数量:\033[0m")
            buy_num = int(buy_num)
            if p_stock >= buy_num:
                while True:
                    settle=input("\033[37;1m您想对商品[%s]立即下单还是加入购物车呢? y立即购买/n加入购物车\033[0m" % p_name)
                    if settle.lower() == "y":
                        total=p_price * buy_num
                        if total <= balance:
                            balance -= total
                            buy_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            goods_buy=(p_name,buy_num,buy_time)
                            order.append(goods_buy)
                            p_stock-=buy_num
                            print("恭喜您购买成功！详细信息请点击我的订单查询！")
                        else:
                            print("您的余额为[%d] 不足以支付!" % balance)
                        break
                    elif settle.lower() == "n":
                        goods_cart = [p_name, buy_num, p_price]
                        cart.append(goods_cart)
                        print("您的商品[%s]已加入购物车,您随时都可以对它进行结算!" % p_name)
                        break
                    else:
                        print("您输入的有误，请重新输入！")
                        continue
            else:
                print("您选购的商品[%s]库存不足，请选择其他商品！" % p_name)
#查看用户购物记录函数
def record_func(user):
    record=eval(cf.get(user,"order"))
    for index,items in enumerate(record):
        print("\033[31;1m[%d]\033[0m [%s]您好，您在[%s]买了[%d]件商品[%s]" % (index,user,items[2],items[1],items[0]))
#购物车函数(此函数可以实现查看购物车,修改购物车,购物车商品结算,清空购物车等功能)
def cart_func(user):
    cart=eval(cf.get(user,"cart"))
    order=eval(cf.get(user,"order"))
    balance=int(cf.get(user,"salary"))
    print("\033[33;7m您的购物车如下\033[0m".center(50))
    print("编号", "商品".center(20), "数量".center(20),"价格")
    for index,items in enumerate(cart):
        print(index,items[0].center(20),str(items[1]).center(20),items[2])
    exit_flag=False
    while not exit_flag:
        opera=input("请输入您要进行的操作：A 结算 B 修改购物车 C 清空购物车 D 退出购物车 E 查看购物车")
        if opera.upper() == "A":
            total=0
            stock_dict={}
            for goods_info in cart:
                name=goods_info[0]
                num=goods_info[1]
                price=goods_info[2]
                total += price * num
                stock = int(cf.get("库存", name))
                stock -= num
                stock_dict[name]=str(stock)
            if balance >= total:
                balance -= total
                buy_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for goods_info in cart:
                    name_buy=goods_info[0]
                    num = goods_info[1]
                    goods_buy = (name_buy, num, buy_time)
                    order.append(goods_buy)
                cart.clear()
                for k in stock_dict:
                    cf.set("库存", k, stock_dict[k])
                cf.set(user, "order", str(order))
                cf.set(user, "salary", str(balance))
                cf.set(user, "cart", str(cart))
                cf.write(open(db, "w"))
                print("购物车商品%s已全部结算，详细请查看您的订单！" % str(name))
            else:
                print("抱歉，您的余额【%d元】不足以支付订单【%d元】" % (balance,total))
        elif opera.upper() == "B":
            hand=input("请问您是要修改商品数量还是要删除商品呢? A 修改商品数量 B 删除商品")
            if hand.upper() == "A":
                number=int(input("\033[37;1m请输入您要修改的商品的编号:\033[0m"))
                print("现在购物车里有[%d]件[%s]" % (cart[number][1],cart[number][0]))
                num_new=input("\033[37;1m请输入您要购买的数量:\033[0m")
                cart[number][1]=int(num_new)
            if hand.upper() == "B":
                number=int(input("\033[37;1m请输入您要删除的商品的编号:\033[0m"))
                cart.pop(number)
            cf.set(user, "cart", str(cart))
            cf.write(open(db, "w"))
            print("修改购物车成功!")
        elif opera.upper() == "C":
            cart.clear()
            cf.set(user, "cart", str(cart))
            cf.write(open(db, "w"))
            print("清空购物车成功!")
        elif opera.upper() == "D":
            exit_flag=True
        elif opera.upper() == "E":
            cart = eval(cf.get(user, "cart"))
            order = eval(cf.get(user, "order"))
            balance = int(cf.get(user, "salary"))
            print("\033[33;7m您的购物车如下\033[0m".center(50))
            print("编号", "商品".center(20), "数量".center(20), "价格")
            for index, items in enumerate(cart):
                print(index, items[0].center(20), str(items[1]).center(20), items[2])
        else:
            print("您的输入有误,请重新输入!")
#充值函数,可以查看余额,也可以充值
def charge_func(user):
    balance=int(cf.get(user,"salary"))
    print("您当前的余额为[%d元]" % balance)
    while True:
        money=input("\033[37;1m请输入您要充值的金额:\033[0m")
        if money.isdigit():
            balance+=int(money)
            cf.set(user,"salary",str(balance))
            cf.write(open(db,"w"))
            print("恭喜您充值成功!余额为[%d元]" % balance)
            break
        else:
            print("您输入的有误,请重新输入!")

#shop_func("zy")
#cart_func("zy")
#record_func("zy")
#charge_func("zy")

if __name__ == "__main__":
    mail_check()
    login_info=login()
    login_flag=login_info[0]
    username=login_info[1]
    while True:
        operate=input("\033[37;1m请输入您要进行的操作:A 购物 B 进入购物车 C 查看购物信息 D 充值 E 退出 \033[0m")
        if operate.upper() == "A":
            shop_func(username)
        if operate.upper() == "B":
            cart_func(username)
        if operate.upper() == "C":
            record_func(username)
        if operate.upper() == "D":
            charge_func(username)
        if operate.upper() == "E":
            sys.exit("欢迎您的下次光临")



