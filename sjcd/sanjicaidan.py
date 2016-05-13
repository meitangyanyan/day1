#/usr/bin/env python
#-*- coding:utf-8 -*-
#Authot:Zhang Yan

from map import province,city,county
import sys

province_new={}
def province_func():
    for i in province:
        province_new[int(i)]=province[i]
    return province_new

city_new={}
def city_func(i):
    for j in city:
        if j.split('-')[0] == i:
            city_new[int(j.split('-')[1])]=city[j]
    return city_new

county_new={}
def county_func(i,j):
    city_func(i)
    for k in county:
        if k.split('-')[0] == i and k.split('-')[1] == j:
            county_new[int(k.split('-')[2])]=county[k]
    return county_new


def show_func(m,num=0,name="a",level="a"):
    if m == "a":
        print("#"*80)
        print("\033[31;7m欢迎您阅览中国地图!\033[0m".center(85))
        print("#"*80)
    if m == "b":
        print("-"*33+"\033[35;1m开++始++查++询\033[0m"+"-"*33)
    if m == "c":
        print("-"*33+"\033[35;1m结++束++查++询\033[0m"+"-"*33)
    if m == "d":
        print("编号:%d".center(40) % num + "%s:%s".center(40) % (name,level))
    if m == "e":
        print("#" * 80)
        print("\033[33;7m欢迎您的下次光临!\033[0m".center(85))
        print("#" * 80)

def menu1_func():
    print("-" * 33 + "\033[35;1m第 一 级 菜 单\033[0m" + "-" * 33)
    print("\033[32;1m***中国的省有:\033[0m")
    pro = province_func()
    for x in pro:
        show_func("d", x, "省", pro[x])

def menu2_func(pro_num):
    print("-" * 33 + "\033[35;1m第 二 级 菜 单\033[0m" + "-" * 33)
    pro=province_func()
    if int(pro_num) in pro:
        show_func("b")
        print("\033[32;1m***%s的市有:\033[0m" % pro[int(pro_num)])
        city1 = city_func(pro_num)
        for y in city1:
            show_func("d", y, "市", city1[y])
        show_func("c")
        city1.clear()
    else:
        return True

def menu3_func(pro_num,city_num):
    print("-" * 33 + "\033[35;1m第 三 级 菜 单\033[0m" + "-" * 33)
    city1 = city_func(pro_num)
    if int(city_num) in city1:
        show_func("b")
        print("\033[32;1m***%s的县有:\033[0m" % city1[int(city_num)])
        county1 = county_func(pro_num,city_num)
        for z in county1:
            show_func("d", z, "县", county1[z])
        show_func("c")
        county1.clear()
    else:
        return True

def opera_func():
    show_func("a")
    while True:
        menu1_func()
        pro_num = input("\033[38;1m请输入您要查看的省的编号:\033[0m")
        if pro_num.isdigit():
            while True:
                if menu2_func(pro_num):
                    print("\033[31;7m您查看的省不在我们的字典中!请重新输入!\033[0m")
                    break
                city_num = input("\033[38;1m请输入您要查看的市的编号(如果输入a则返回上一层):\033[0m")
                if city_num.lower() == "a":
                    break
                elif city_num.isdigit():
                    while True:
                        if menu3_func(pro_num, city_num):
                            print("\033[31;7m您查看的市不在我们的字典中!请重新输入!\033[0m")
                            break
                        hand=input("\033[34;1m您已到达最后一级菜单,您可以:A 返回上一级 B 退出\033[0m")
                        if hand.upper() == "A":
                            break
                        elif hand.upper() == "B":
                            show_func("e")
                            sys.exit()
                        else:
                            print("\033[31;1m您的输入有误,请重新输入!\033[0m")
                            continue
                else:
                    print("\033[31;1m您的输入有误,请重新输入!\033[0m")
                    continue
        else:
            print("\033[31;1m您的输入有误,请重新输入!\033[0m")
            continue

if __name__ == "__main__":
    opera_func()

















