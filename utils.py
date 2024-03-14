#!/user/bin/env python
# -*- coding:utf-8 -*-
# @Time     : 10/24/2020
# @Author   : Chen
# ---------------------
import collections
from collections import namedtuple as nt
import os
import re
import string

lift_path="z.txt"
#q_s_k = nt('q_s_k', ['question', 'select', 'key'],defaults=("",tuple(),""))


class elevator_question(object):
    q_s_k = nt('q_s_k', ['question', 'select', 'key'],defaults=("",tuple(),""))
    def __init__(self,file_path=lift_path,reg_option=None,reg_option_spilt=None,reg_select=None):
        self.reg_option,self.reg_select,self.file_path,self.reg_option_spilt=reg_option,reg_select,file_path,reg_option_spilt
        self.ques_txt, self.ques_dict = self.getQues_()

    def getQues_(self):
        reg_option = re.compile(r"(A\..*?)正确答案：") if self.reg_option is None else re.compile(self.reg_option)
        reg_option_ = re.compile(r"。（([对错])）$") if self.reg_select is None else re.compile(self.reg_select)
        reg_option_spilt = re.compile(r" [ABCD]\.") if self.reg_option_spilt is None else re.compile(reg_option_spilt)
        
        i = 0
        line_tmp = ""
        ques_dict = {}
        ques_txt = {}
        judge_select=("A.对","B.错")
        # 题目生成： 格式：{1: '《特种设备安全监察条例》中所称的特种设备是指涉及( )安全、...', 2: '持证作业人员违章操作或者管理造成特种设备特大事故的，吊销《特种设备作业人员证》，
        with open(self.file_path, 'r', encoding="utf-8")as f:
            data_list = f.readlines()

        for line in data_list:
            if line == "\n":        # 请设置 空行 为每一题的分割符号
                ques_txt[i] = line_tmp
                i += 1
                line_tmp = ""
            elif len(line) >= 2 and line.endswith("\n"):
                line_tmp += line[0:-1]

        # 获取题目数量
        j, k = 1, 1
        for k, v in ques_txt.items():
            if "正确答案：" in v:
                j += 1
            elif "（对）" in v or "（错）" in v:
                k += 1
            else:   # 没有答案的题目，这表示分割出错了
                print(k,v)    
                raise Exception("data formatting error, please debug here!")
        
        # 题目内容 选项内容 正确答案
        for k, v in ques_txt.items():
            if "正确答案" in v and "A." in v:  # 选择题
                ques_txt[k] = v.replace("A.", "\nA.").replace("正确答案", "\n正确答案")
                question_option = reg_option.findall(v)[0]
                tmp_data = v.split(question_option) # tmp_data 为 题目和答案
                # assert len(tmp_data) <= 2   # 答案数必须小于 2
                temp_spilt=re.split(reg_option_spilt,question_option)
                for index,syn in enumerate(string.ascii_uppercase[1:len(temp_spilt)],1):
                    temp_spilt[index]=f"{syn}.{temp_spilt[index]}"
                ques_dict[k]=self.q_s_k(tmp_data[0],tuple(temp_spilt),f'\n{tmp_data[1].strip("正确答案：")}')

            # 题目内容：判断内容 选项内容 正确答案           
            else :
                ques_dict[k]=self.q_s_k(v[0:-3],judge_select,"对" if v.endswith("。（对）") or "（对）" in v[-5:] else "错" )
        if len(ques_dict)==len(ques_txt):
            return ques_txt, ques_dict
        else:
            raise Exception("data formatting error, please debug here!")

    # 根据关键词查找 题目 ：
    def getQuestionByKeyWord(self, keyord: str):
        k_list = [k for k, v in self.ques_txt.items() if keyord in v]
        return {k: self.ques_dict[k] for k in k_list}


class words_option(elevator_question):

    def __init__(self):
        super().__init__()
        '''
        the data source is from ../subject_text/z.txt ==> is processed by class : elevator_question 
        
        # we can use the variable :self.ques_txt , self.ques_dict by extends elevator_question class.
            self.ques_txt : dict variable : {1: '要用晶体三极管实现电流放大，必须使（ ）处于正向偏置。\nA.发射结 B.集电结 C.控制极 D.阳极\n正确答案：A',  ...}
            self.ques_dict : This variable is more efficient than self.ques_txt : {1: q_s_k(question='要用晶体三极管实现电流放大，必须使（ ）处于正向偏置。', select='A.发射结 B.集电结 C.控制极 D.阳极', key='\n正确答案：A'), 
        '''
        # print(len(self.ques_txt),len(self.ques_dict))   # 1261 1261

    def getSomeDataOfElevator(self)->dict:
        f'''
        :return: a dict just like: :  [for i in num_data]:[index of self.ques_dict.keys()]
        '''
        # some number must be use in question and select options:

        # not implemented ==> wait for me update next time : ################################################################
        time_data=["一","二","三","四","五","六","七","八","九","十"]+list(range(0,10))

        num_data=['m','s','℃','g','n','Ｎ','/','~','～','v','w','倍','比','±','％','x','Φ','Ω',"种",'dB','db',"于"]
        data1=collections.defaultdict(list)
        [data1[i].append(j) for i in num_data for j in self.ques_dict.keys() if i in self.ques_dict[j].question.lower() or i in self.ques_dict[j].select.lower()]
        return data1    # key:index of questions

if __name__ == "__main__":
    pass    # utils.elevator_question().ques_dict[index]
    
    data=elevator_question().ques_dict
    txt=elevator_question().ques_txt
    print(txt)
    '''
    with open("demo.txt",'w',encoding="utf-8") as f:
        for i in range(len(data)):
            print(str(data[i].key),file=f,end="")
    '''
