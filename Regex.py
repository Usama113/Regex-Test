import re
import numpy as np


def input_type(i):#to check the type of input
    if(ord(i)>=48 and ord(i)<=57):
        return 1;
    elif((ord(i)>=65 and ord(i)<=90) or (ord(i)>=97 and ord(i)<=122)):
        return 2;
    else:
        return 3;

def regex_form_string(str):#to encode input to regex form
    delimeter='.'
    str_temp=""

    for i in str:
        if(input_type(i)==1):
            str_temp=str_temp+"\d"+delimeter
        elif(input_type(i)==2):
            str_temp=str_temp+'\w'+delimeter
        elif(input_type(i)==3):
            str_temp=str_temp+i+delimeter

    return str_temp

def regex_digit_form(digit):#calculate the consecutive symbols
    reg_len=len(digit[0].split('.'))

    temp1=(digit.split('.')[0:-1])
    temp=[int(i) for i in temp1]

    return temp


def outlier_removal(d,reg,digits,pattern):#remove the outliers(pattern based)
    pattern_len=[len(x) for x in pattern]
    pattern_set=set(pattern_len)
    pattern_len=np.array(pattern_len)
    ls_temp=[]
    for i in pattern_set:
        idx=pattern_len==i
        ls_temp.append(np.sum(idx))

    m=max(ls_temp)
    j=0
    for i in ls_temp:
        if(m==i):
            break;
        j=j+1

    max_value=list(pattern_set)[j]
    idx=pattern_len==max_value
    return np.array(d)[idx].tolist(),np.array(reg)[idx].tolist(),np.array(digits)[idx].tolist(),np.array(pattern)[idx].tolist()







def word_identifier(d,digits,pattern,k):#identifying uppercase, lower case, or specific letters
    ls_temp=[]
    l=0
    for i in d:
        index=0
        for j in range(k):
            if(pattern[l][j]==-1):
                index=index+1
            else:
                index=index+digits[l][j]

        ls_temp.append(i[index:index+digits[l][k]])
        l = l + 1

    temp_len=np.array([len(x) for x in ls_temp])
    if(np.sum(temp_len==1)==temp_len.shape[0]):
        max_word=max(ls_temp)
        min_word=min(ls_temp)
        temp=0
        for i in range(ord(min_word),ord(max_word)):
            if(ls_temp.index(chr(ord(min_word)+temp))!=-1):
                temp=temp+1
            else:
                return_ls=[1]
                if(ord(min_word)>=65 and ord(min_word)<=90):
                    return_ls.append(1)
                else:
                    return_ls.append(0)

                if(ord(min_word)>=97 and ord(min_word)<=122):
                    return_ls.append(1)
                else:
                    return_ls.append(0)
                return return_ls
        if(temp==ord(max_word)-ord(min_word)):
            return [2,ord(min_word),ord(max_word)]
    else:
        count=0
        count1=0
        for i in ls_temp:
            if(i.isupper()):
                count=count+1
            if(i.islower()):
                count1=count1+1

        if(count==len(ls_temp)):
            return [3,1,0]
        elif(count1==len(ls_temp)):
            return [3,0,1]


        return [3,1,1]










def regex_formation(d,reg,digits,pattern):#generating the final regex of string
    d,reg,digits,pattern=outlier_removal(d,reg,digits,pattern)

    min=np.min(digits,axis=0)
    max=np.max(digits,axis=0)
    temp=reg[0].split('.')[0:-1]
    #temp1=pattern[0]
    regex_temp=''
    regex_temp1=''
    regex_temp2=''
    score = 1.00
    score1 = 100
    score2 = 100

    k=0
    for i in temp:
        if(score<0.50):
            score=0.50
        if(input_type(i[-1])==3):
            regex_temp=regex_temp+i
            regex_temp1=regex_temp1+i
            regex_temp2 = regex_temp2 + i
            k=k+1



        else:
            if(i[-1]=='d'):
                if(min[k]==max[k]):
                    regex_temp = regex_temp + i + '{' + str(min[k]) + '}'
                    regex_temp1 = regex_temp1 + i + '{' + str(min[k]-1)+','+ str(max[k]+1)+ '}'
                    regex_temp2 = regex_temp2 + '\d+'

                else:
                    regex_temp=regex_temp+i+'{'+str(min[k])+','+str(max[k])+'}'
                    regex_temp1 = regex_temp1 + i + '{' + str(min[k]-1) + ',' + str(max[k]+1) + '}'
                    regex_temp2 = regex_temp2 + '\d+'

                score1 = score1 - 10*score
                score2 = score2 - 20*score
                score=score-0.25
            else:
                res_temp=word_identifier(d,digits,pattern,k)
                if (res_temp[0] == 2):

                    if(res_temp[1]!=res_temp[2]):
                        regex_temp = regex_temp + '['+chr(res_temp[1])+chr(res_temp[2])+']'
                        if(res_temp[1]>=65 and res_temp[1]<=90):
                            regex_temp1 = regex_temp1 + '[' + 'A-Z' + ']'
                        else:
                            regex_temp1 = regex_temp1 + '[' + 'a-z' + ']'
                        regex_temp2 = regex_temp2 + '\w+'
                        score1 = score1 - 10
                        score2 = score2 - 20
                    else:
                        regex_temp = regex_temp + chr(res_temp[1])
                        if (res_temp[1] >= 65 and res_temp[1] <= 90):
                            regex_temp1 = regex_temp1 + '[' + 'A-Z' + ']'
                        else:
                            regex_temp1 = regex_temp1 + '[' + 'a-z' + ']'
                        regex_temp2 = regex_temp2 + '\w+'
                        score1 = score1 - 10
                        score2 = score2 - 20

                elif(res_temp[0]==1):
                    temp2=''
                    if(res_temp[1]==1 ):
                        temp2=temp2+'A-Z'
                    if(res_temp[2]==1):
                        temp2=temp2+'a-z'
                    regex_temp = regex_temp + '[' + temp2 + ']'
                    regex_temp1 = regex_temp1 + '[' + 'A-Za-z' + ']'
                    regex_temp2 = regex_temp2 + '\w+'
                else:
                    temp2 = ''
                    if (res_temp[1] == 1):
                        temp2 = temp2 + 'A-Z'
                    if (res_temp[2] == 1):
                        temp2 = temp2 + 'a-z'

                    if (min[k] == max[k]):
                        regex_temp = regex_temp +'[' + temp2 +']' + '{' + str(min[k]) + '}'
                        regex_temp1 = regex_temp1 + '[' + temp2 + ']' + '{' + str(min[k] - 1) + ',' + str(max[k] + 1) + '}'
                        regex_temp2 = regex_temp2 + '\w' + '{' + str(min[k]-1) + ',' + str(max[k]+1) + '}'

                    else:
                        regex_temp = regex_temp +'[' + temp2 +']' + '{' + str(min[k]) + ',' + str(max[k]) + '}'
                        regex_temp1 = regex_temp1 + '[' + temp2 + ']' + '{' + str(min[k] - 1) + ',' + '}'
                        regex_temp2 = regex_temp2 + '\w+'

                score1 = score1 - 10 * score
                score2 = score2 - 20 * score
                score = score - 0.25
            k=k+1
    if(score1<30):
        score1=30
    if(score2<20):
        score2=20
    return (regex_temp,100),(regex_temp1,score1),(regex_temp2,score2)

def regex_form(ls):
    delimeter='.'
    ls=ls.split('.')
    reg_temp=''
    digits_temp=''
    pattern_temp=[]
    count=1
    temp=ls[0]
    i=len(ls)
    for j in range(1,i):
        if(ls[j]==temp):
            count=count+1
        else:
            if(input_type(temp[-1])==3):
                reg_temp = reg_temp + temp+delimeter
                digits_temp=digits_temp+str(-1)+delimeter
                pattern_temp.append(-1)
            else:
                if(temp[-1]=='w'):
                    pattern_temp.append(2)
                elif(temp[-1]=='d'):
                    pattern_temp.append(1)
                #reg_temp=reg_temp+temp+'{'+str(count)+'}'
                reg_temp = reg_temp + temp+delimeter
                digits_temp=digits_temp+str(count)+delimeter
            count=1
            temp=ls[j]

    return reg_temp,digits_temp,pattern_temp


def string_to_regex(ls):#intermediatry regex form
    ls_temp=[]
    pattern_temp=[]
    digits_temp1=[]
    for i in ls:
        temp=regex_form_string(i)
        reg,digit,pattern=regex_form(temp)
        ls_temp.append(reg)
        temp=regex_digit_form(digit)
        digits_temp1.append(temp)
        pattern_temp.append(pattern)

    return ls_temp,digits_temp1,pattern_temp




def value_matching(d):#task1
    res, res_digit, res_pattern = string_to_regex(d)

    result, result1, result2 = regex_formation(d, res, res_digit, res_pattern)
    print("(r'^"+result[0]+"$',"+str(result[1])+')')
    print("(r'^" + result1[0] + "$'," + str(result1[1]) + ')')
    print("(r'^" + result2[0] + "$'," + str(result2[1]) + ')')
    return [result, result1, result2]

def value_extraction(d):#task2
    d1=[]
    d2=[]
    for i in d:
        d1.append(i[0])
        d2.append(i[1])
    res1, res_digit1, res_pattern1 = string_to_regex(d1)
    result11= regex_formation(d1, res1, res_digit1, res_pattern1)

    res2, res_digit2, res_pattern2 = string_to_regex(d2)
    result22= regex_formation(d2, res2, res_digit2, res_pattern2)

    #print(result11[0][0].replace(result22[0][0],'('+result22[0][0]+')'))
    print('#################')
    result=(result11[0][0].replace(result22[0][0],'('+result22[0][0]+')'),result11[0][1])
    result1 = (result11[1][0].replace(result22[1][0], '(' + result22[1][0] + ')'), result11[1][1])
    result2 = (result11[2][0].replace(result22[2][0], '(' + result22[2][0] + ')'), result11[2][1])
    print("(r'^" + result[0] + "$'," + str(result[1]) + ')')
    print("(r'^" + result1[0] + "$'," + str(result1[1]) + ')')
    print("(r'^" + result2[0] + "$'," + str(result2[1]) + ')')
    return [result,result1,result2]


def main():

    d=["a-1012331/1",
        "a-1231141/2",
        "a-1231141/1",
        "a-1233441/2",
        "a-1231321/3",
        "b-1231141/11"]

    d1=[("A-1012331/1", "1012331"),
        ("A-1231141/2", "1231141"),
        ("A-1231141/1", "1231141"),
        ("A-1233441/2", "1233441"),
        ("A-1231321/3", "1231321"),
        ("B-1231141/11", "1231141")]
    value_matching(d)
    value_extraction(d1)

if __name__ == '__main__':
    main()