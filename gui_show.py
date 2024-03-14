# -*-codings:utf-8-*-

import sys  # 116
import os
sys.path.append(os.path.dirname(__file__))
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"

import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import re
import sqlite3
import random
import datetime
import utils
import time
from collections import namedtuple as nt,defaultdict,OrderedDict
from tkinter.constants import (HORIZONTAL, VERTICAL, RIGHT, LEFT, X, Y, BOTH, BOTTOM, YES, NONE, END, CURRENT)
from functools import partial
import textwrap


# question infomation variable :
question_num=100  # test user num
question_data=utils.elevator_question().ques_dict
question_score=1 # every question score value

root=tk.Tk() # the root window
# assembly variable
Label=partial(tk.Label,master=root)
Button=partial(tk.Button,master=root)
Entry=partial(tk.Entry,master=root)
Radiobutton=partial(tk.Radiobutton,master=root)
Checkbutton=partial(tk.Checkbutton,master=root)
StringVar=tk.StringVar
X=tk.X

# modules list
modules_dict=defaultdict(dict)
# label_modules,input_modules,btn_modules,radio_modules,checkbox_modules=[list() i for i in range(5)]
input_vars=[StringVar() for i in range(10)]
font1=("Times New Roman",12)
font2=("微软雅黑",15)
font3=("隶书",20)
font4=("黑体",27)
font5=("黑体",20)
font6=("微软雅黑",15)


# get windows coordinate  ==> this function must be in front of root=tk.Tk() and root.mainloop()
def set_windowsAxis():
    # this funcion can do dynamic label for root window
    try:
        _label_m=modules_dict['label_modules']
        if _label_m.get("system_time"):
            _label_m["system_time"].configure(text=f"当前系统时间： {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if start_test and _label_m.get("user_time"):
            _label_m["user_time"].configure(text=f"您已经用时: {int((time.time()-start_test)//60)} 分钟")
    except Exception as e:
        raise 
        print("第59~69行报错:",e)
    root.after(10,set_windowsAxis)


def clear_modules():
    for widget in root.winfo_children():
        widget.destroy()
    modules_dict.clear()
    [i.set("") for i in input_vars]


def test(func):         # valid the user login input .
    def wrapper(*args,**kwargs):
        _reg=[re.compile(r"^[5a-zA-Z0-9_]{3,20}$"),re.compile(r"^[a-zA-Z0-9_-]{4,16}$"),re.compile(r"^((13[0-9])|147|15([0-3]|[5-9])|(17[3,6,7,8])|(18[0-9])|(19[1,9]))\d{8}$"),re.compile("[男女]"),re.compile(r"^[1234567]$")]
        for index,reg_ in enumerate(_reg):
            if reg_.match(input_vars[index].get()) is None: 
                messagebox.showerror(title="输入出错!",message="用户名3-20位,密码4-16位,正确电话号码,班级1~7之间才能通过!")
                return False
        else:
            return func(*args,**kwargs)
    return wrapper


def get_indexAnd_q_s_k(num:int)->tuple:
    total=len(question_data)
    ll=[] # question index
    question_key=[]
    if num<=total:
        lis=list(range(total))
        for i in range(num):
            ll.append(random.choice(lis))
    else:
        raise Exception("设置考试题目数超过 总题目数，请重新设置！")
    
    ll.sort()
    for i in ll:
        question_key.append(question_data[i].key.strip())
    return tuple(ll),tuple(question_key)


def search(username:str,od:OrderedDict,hidden_label:Label)->None:
    if username in od.keys():
        user=od[username]
        hidden_label.configure(text=f"用户名：{user.name},多次测试平均成绩:{user.average_score} 分,最后测试时间：{user.last_test}\n,平均用时:{user.e_seconds} 秒,共做题：{user.question_num} 道,测试次数:{user.test_times} 次")
    else:
        messagebox.showerror(title="no such user!",message="没有找到该用户")


def rank_score(text:Text)->OrderedDict:
    text.config(state="normal")
    text.delete("1.0",'end')
    
    l=['name', 'average_score', 'last_test', 'e_seconds', 'question_num','test_times']
    users=nt("users",l)
    dic_users=defaultdict(list)
    dic_user=defaultdict(list)
    s_n=defaultdict(str)
    od=OrderedDict()

    conn=sqlite3.connect("student_data.db")
    cur=conn.cursor()

    try:
        # get all test for a user
        data=cur.execute(f"select stu_info.name,score_info.score,score_info.create_time,score_info.take_second,score_info.question_num from stu_info,score_info where stu_info.sid==score_info.stu_id;").fetchall()
        # # you also can use database sql to get data for average data here, here just for python to do it
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    # 我也不知道当初这里是想干嘛,怎么计算的,但是先就这样吧!
    for index,tup in enumerate(data,0):
        dic_users[tup[0]].append(users(*tup,1))
        dic_user[tup[0]]=[tup[0],0,tup[2],0,0] # there is three value must calc
    
    for key, value in dic_users.items():
        print(len(value))
        for i,tup in enumerate(value,1):
            if i!=2 or i<=4:dic_user[key][i] += int(tup[i]/len(dic_users[key]))
            else:continue  
        dic_user[key].append(len(dic_users[key]))
        dic_user[key]=users(*dic_user[key])

    # use user score as key ,name as value make a dict for sort
    for key,value in dic_user.items():s_n[value.average_score]=key
    for i in sorted(s_n,reverse=True):od[s_n[i]]=dic_user[s_n[i]]

    text.insert('1.0',"".join([f"{str(i)[:13]:<16}" for i in l])+"\n")
    for index,value in enumerate(od.values(),3): # key : user_name
        text.insert(f"{float(index)}","".join([f"{str(i)[:13]:<16}" for i in value])+"\n")
        
    text.config(state='disable')  # inhibit edit the text
    return od


def save_socre(data:list,new_score:int,question_index:list,minutes:int)->None:
    conn = sqlite3.connect("student_data.db")
    cur = conn.cursor()
    try:
        date_time=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        cur.execute(f"insert into score_info (create_time,take_second,score,stu_id,course_id,question_num,index_list) values ('{date_time}',{minutes//60+1},{new_score},{data[5]},1,{question_num},'{str(question_index)}');")
        cur.execute(f"update stu_info set score='{new_score}',minutes='{minutes//60+1}',question_num={question_num} where sid={data[5]}")
        conn.commit()
        show_scoreRangk([*data[:-1],new_score,minutes])
    except Exception as e:
        raise 
        print(e,"第187行报错:数据入库出错")
    finally:
        cur.close()
        conn.close()


def valid_input(no:int,no_q:int,user_key:defaultdict)->bool:
    # 判断用户未做
    if len(input_vars[0].get())!=0 :    # single select or judge
        user_key[(no,no_q)]=input_vars[0].get()
    elif any([input_vars[i].get() for i in range(1,10)]):  
        temp="".join([i.get() for i in input_vars])
        user_key[(no,no_q)]=temp
    else:   # user input wrong answer and there is no answer before.
        messagebox.showerror(title="您没做当前题", message="请选好当前选项后再往后或往前切题！")
        return False
    return True


def distory_rb_cb(u_key:str): 
    if len(u_key)>=10:u_key=""  # 多选再多也不会超过 10 个吧
    _radio_modules=modules_dict['radio_modules']
    _checkbox_modules=modules_dict['checkbox_modules']
    for rb in _radio_modules.values():
        rb.destroy()
    _radio_modules.clear()
    for cb in _checkbox_modules.values():
        cb.destroy()
    _checkbox_modules.clear()
    [i.set("")for i in input_vars]
    if len(u_key)==1:          # 当用户切换到已经做过的题目时，给选项设置用户做过的选择
        input_vars[0].set(u_key)
    else:
        for index,syn in enumerate(u_key,1):
            input_vars[index].set(syn)


def show_select(no:int,no_q:int,user_key=defaultdict(str)):
    _radio_modules=modules_dict['radio_modules']
    _checkbox_modules=modules_dict['checkbox_modules']

    q_s_k=question_data[no_q]   # question data (question,select,key)
    qsk_k=q_s_k.key.strip() # the real answer 
    input_v=input_vars[0]
    relx=0.15
    rely=0.35
    distory_rb_cb(user_key[(no,no_q)])

    if len(qsk_k)==1:   # single answer and make user can only select one Radiobutton
        #print("进入单选题")
        for index,context in enumerate(q_s_k.select,0):
            if qsk_k in "对错":
                _radio_modules[index]=Radiobutton(text=context,value=context[-1],font=font3,variable=input_v)
            else:
                _radio_modules[index]=Radiobutton(text=context,value=context[0],font=font3,variable=input_v)
            _radio_modules[index].place(relx=relx,rely=rely+index/10)
    else:
        #print("进入复选框")
        for index,context in enumerate(q_s_k.select,0):
            print(context,context[0])
            _checkbox_modules[index]=Checkbutton(text=context,variable=input_vars[index+1],onvalue=context[0],offvalue="",font=font3)
            _checkbox_modules[index].place(relx=relx,rely=rely+index/10)


def repaint_root(data:list):
    global start_test
    start_test=None
    clear_modules()
    root.resizable(1,1)
    root.geometry("800x800")
    no=1    # the current question number !
    STATE="state"
    DISABLED="disabled"
    NORMAL="normal"
    last_q_b=None
    submit_b=None
    next_q_b=None
    modules_dict=defaultdict(dict)
    _relx=0.1
    _rely=.75
    _padx=35
    _pady=15
    _txt_len=45

    user_key=defaultdict(str) # the user answer dict: {(no,no_question[index]):str]}
    no_question,question_keys=get_indexAnd_q_s_k(question_num)  # the question_num question infomation and key of those questions
    
    _label_m=modules_dict['label_modules']
    
    root.title(f"欢迎您: {data[0]},请在这里开始测试吧！")
    Label(text=f'位于 L0{data[4]} 班的 {data[0]} 同学，你好，请用心答题！',font=(font3[0],23),bg='green').pack(fill=X,pady=0)
    Button(text="注 销", command=login_create, font=font1).pack(padx=_padx,pady=_pady,side='right', anchor='nw')
    _label_m["system_time"]=Label(text=f"当前系统时间： {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",font=font2)
    _label_m["system_time"].place(relx=_relx,rely=_rely/6)
    
    txt="\n".join(textwrap.wrap(question_data[no_question[no-1]].question.strip(), width=_txt_len)) # 这样写没有用,windows 上依旧给你占满咯
    ques_context_l=Label(text=f"{no}.{txt}",font=font4, fg="blue")
    ques_context_l.place(relx=_relx,rely=_rely/3.5)

    # First question show 
    show_select(no,no_question[no-1],user_key)
    
    _label_m["user_time"]=Label(text=f"计时已开始，您已用时: 0 分钟",font=font3)
    _label_m["user_time"].place(relx=_relx,rely=_rely*1.24)

    start_test=time.time()
    set_windowsAxis()   # system time dynamic show

    hidden_l=Label(text=f"", font=font5, fg='green') # 这里是隐藏的数据(当前题目答案)
    hidden_l.place(relx=_relx*1.2, rely=_rely)

    def change_question(pre_next:bool=False)->None:    # go to next question when pre_next is False
        nonlocal no
        show_answer("")
        if valid_input(no,no_question[no-1],user_key) is False:return
        if pre_next:no-=1
        else:no+=1
        if no==1:
            last_q_b[STATE]=DISABLED
        elif no==question_num:
            next_q_b[STATE]=DISABLED
            submit_b[STATE]=NORMAL
        else:
            last_q_b[STATE]=NORMAL
            next_q_b[STATE]=NORMAL
        txt="\n".join(textwrap.wrap(question_data[no_question[no-1]].question.strip(), width=_txt_len)) 
        ques_context_l.configure(text=f'{no}. {txt}')
        show_select(no,no_question[no-1],user_key)

    def user_submit():
        nonlocal no
        score=0
        wrong_index=[]
        if len(user_key)<=question_num:
            if valid_input(no,no_question[no-1],user_key) is False:return  # the last question do not answer 
            for (index,_),key in user_key.items():  # start calc score
                if key.strip()==question_keys[index-1].strip():
                    score+=question_score
                else:
                    wrong_index.append(index)
            messagebox.showinfo(title="本次测试得分",message=f"本次模拟{question_num}道题，每道题 {question_score} 分,您的得分: {score}")
            save_socre(data,score,wrong_index,int((time.time()-start_test)))  # [chen 123456 15527480318 1 1 sid scroe_old question_num]
        else:
            raise Exception("用户的答题卡异常，超出出题数目，待重新检查代码")

    def show_answer(true_key:str):
        if true_key!="":
            hidden_l.configure(text=f"正确答案: {true_key}")
        else:
            hidden_l.configure(text=f"")

    # button : 注销 上一题 结束测验 下一题 答案
    last_q_b=Button(text="上一题", font=font2, command=lambda: change_question(True))
    last_q_b[STATE]=DISABLED
    last_q_b.place(relx=_relx,rely=_rely*1.1)

    submit_b=Button(text="提  交", font=font2, command=user_submit)
    submit_b[STATE]=DISABLED
    submit_b.place(relx=_relx*3, rely=_rely*1.1)

    next_q_b=Button(text="下一题", font=font2, command=lambda:change_question())
    next_q_b.place(relx=_relx*5, rely=_rely*1.1)
    answer_b=Button(text="答  案", font=font2, command=lambda:show_answer(question_keys[no-1]))
    answer_b.place(relx=_relx*7, rely=_rely*1.1)
    soce_rank=Button(text="分数排名",command=lambda :show_scoreRangk(data),font=font1)
    soce_rank.pack(padx=_padx,pady=_pady,side='left', anchor='nw')


def show_scoreRangk(data:list):
    clear_modules()
    root.geometry("1500x860")
    root.title("Rank of student")
    root.state = 'normal'
    root.resizable(1, 1)
    _padx=25
    _pady=10
    _relx=.1
    _rely=.1
    _width=110
    _height=30

    Label(text=f"欢迎您: {data[0]},最近一次测试您的分数: {data[6]}",font=font5,bg='green',fg="blue").pack(fill=X,pady=0.1)
    Button(text="注  销", command=login_create, font=font1).pack(padx=_padx, pady=_pady*2.2, side='right', anchor='nw')
    Button(text="重新考试", command=lambda:repaint_root(data), font=font1).pack(padx=_padx, pady=_pady*2.2, side='right', anchor='nw')
    Label(text="请输入您要查看分数的用户名:",font=font1,fg="green").place(relx=_relx,rely=_rely)

    input_vars[0].set("")
    Entry(textvariable=input_vars[0],font=font3,justify='center',width=int(_width*.4)).place(relx=_relx,rely=_rely*1.5,height=int(_height*1.5))

    sc=Scrollbar(root)
    sc.pack(side="right", fill='y')
    text=Text(width=_width, height=_height, undo=False, font=font5,autoseparators=False,yscrollcommand=sc.set)
    text.place(relx=_relx*.1, rely=_rely*3.5)
    od=rank_score(text)    # show user average score rank

    _hidden_m=Label(text="",font=font2,fg="red")
    _hidden_m.place(relx=_relx,rely=_rely*2.5)
    Button(text="search",font=font3,command=lambda :search(input_vars[0].get(),od,_hidden_m)).place(relx=_relx*7,rely=_rely*1.5)


def select_data(input_name:str,input_phoneNum:str)->tuple:
    conn=sqlite3.connect("student_data.db")
    cur=conn.cursor()
    data=cur.execute(f"select name,password,phoneNum,gender,class_id,sid,score,question_num from stu_info where name='{input_name}' and phoneNum='{input_phoneNum}'").fetchone()
    return conn,cur,data


@test
def register():  # register 
    # get variables for sql to execute
    input_name=input_vars[0].get()
    input_password=input_vars[1].get()
    input_phoneNum=input_vars[2].get()
    input_gender=input_vars[3].get()
    input_class_id=input_vars[4].get()
    conn,cur,data=select_data(input_name,input_phoneNum)    
    if data is None:
        try:
            cur.execute(f"insert into stu_info (name,password,phoneNum,gender,class_id)values('{input_name}','{input_password}','{input_phoneNum}',{0 if input_gender=='男' else 1},{int(input_class_id)})")
            conn.commit()   
            result=messagebox.askquestion(title='登录?',message='注册成功，是否立即登录？') # tkinter.messagebox.showinfo(title="成功",message="注册成功！")
            if result == "yes":  # due to login ?
                cur.close()
                conn.close()
                login([i.get() for i in input_vars])
        except Exception as e:
            print(e)
            result=messagebox.askretrycancel(title='注册失败',message='用户名已存在！,是否删除该帐号并重新注册？')
            if result:
                cur.execute(f"delete from stu_info where name='{input_name}'")
                register()
        finally:
            cur.close()
            conn.close()
    else:
        try:
            cur.close()
            conn.close()
        except Exception as e:
            print(e)
        messagebox.askretrycancel(title='帐号已经存在！',message='帐号已经存在!禁止再次注册')


@test
def login(data:list=None): 
    global no
    # do init for test
    no=1
    if data is not None:
        repaint_root(data)
    else:
        conn,cur,data=select_data(input_vars[0].get(),input_vars[2].get())
        cur.close()
        conn.close()
        if data is None:
            messagebox.showerror(title="用户不存在!",message="请输入正确的用户名,密码和电话号码")
        elif data[1]==input_vars[1].get():
            repaint_root(data)
        else:
            messagebox.showerror(title="密码错误!",message="请输入正确的密码！")


def login_create():     # login_create : the module not need to manager
    clear_modules()
    root.geometry("400x400")
    root.title("register/Login")
    root.state='normal'
    root.resizable(0, 0)

    # for test , do some default value in login
    input_vars[0].set('chen')
    input_vars[1].set("123456")
    input_vars[2].set("15527480318")
    input_vars[4].set('1')
    # delete over code when submit code.

    # ready for variables
    label_names=["UserName ：","Password ：","PhoneNumber：","Gender  ：","Class_id  ："]
    l_x=45;y_=70;e_x=l_x+110;e_width=180;ins=50

    # create modules in window 
    login_lb=Label(text="Student Registration/Login",font=("Times New Roman",24),bg='white')
    login_lb.pack(fill=X,pady=15)

    for index,l in enumerate(label_names):
        # Label create and place
        Label(text=l,font=font1).place(x=l_x,y=y_)
        if index != 3: # create Entry and place 
            dic={'textvariable':input_vars[index],'font':font1,'justify':'center'}
            if index==1: Entry(show="*",**dic).place(x=e_x,y=y_,width=e_width)
            else: Entry(**dic).place(x=e_x,y=y_,width=e_width)
        elif index == 3:
            input_vars[index].set('男')
            for i in [('男',1),('女',1.5)]:
                Radiobutton(text=i[0],value=i[0],font=font1,variable=input_vars[index]).place(x=e_x*i[1],y=y_)
        y_+=ins
    else:
        Button(text="注  册",command=register,font=font6).place(x=e_x/2,y=y_)
        Button(text="登  录",command=login,font=font6).place(x=e_x*1.2+ins,y=y_)

if __name__=="__main__":
    login_create()
    root.mainloop()
