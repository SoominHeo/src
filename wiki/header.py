from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy
import kor_sentence

i=0
number = str(i)

'''
    url for header
'''
header_path = "../../data/wiki/header/{lang}/{idx}.txt"


def remove_tags(data):
    p=re.compile(r'<.*?>')
    return p.sub('', data)

def remove_span(data):
    p=re.compile(r'<span.*>.*?</span>')
    return p.sub('',data)

def remove_comma(data):
    result=data.replace("</p>, <p>"," ")
    return result

def remove_semantic(data):
    p=re.compile(r'<semantics.*>.*?</semantics>',re.S)
    return p.sub('',data)

def remove_brachet(data):
    st_list=[]
    fi_list=[]
    st2_list=[]
    fi2_list=[]
    st=-1
    fi=-1
    st2=-1
    fi2=-1

    # '('를 모두 찾아서 리스트에 인덱스값 저장
    while 1:
        st=data.find('(',st+1)
        if st==-1:
            break
        st_list.append(st)

    # '['를 모두 찾아서 리스트에 인덱스값 저장
    while 1:
        st2=data.find('[' ,st2+1)
        if st2==-1:
            break
        st2_list.append(st2)

    #')'을 모두 찾아서 리스트에 인덱스값 저장
    while 1:
        fi=data.find(')',fi+1)
        if fi==-1:
            break
        fi_list.append(fi)

    #']'을 모두 찾아서 리스트에 인덱스값 저장
    while 1:
        fi2=data.find(']' ,fi2+1)
        if fi2==-1:
            break
        fi2_list.append(fi2)


    # '('와 ')'의 짝에 맞게 매칭시켜서 종속되는 괄호들의 인덱스값은 제거
    for i in range(len(st_list)-2):
        if st_list[i+1]<fi_list[i]:
            del st_list[i+1]
            del fi_list[i]

    # '['와 ']'의 짝에 맞게 매칭시켜서 종속되는 괄호들의 인덱스값은 제거
    for i in range(len(st2_list)-2):
        if st2_list[i+1]<fi2_list[i]:
            del st2_list[i+1]
            del fi2_list[i]

    #'(.......... )' 모두 제거
    result=data
    for j in range(len(st_list)):
        tmp=data[st_list[j]:fi_list[j]+1]
        result=result.replace(tmp,'')

    for j in range(len(st2_list)):
        tmp=data[st2_list[j]:fi2_list[j]+1]
        result=result.replace(tmp,'')

    return result

def remove_bracket(data):

    ck=-1
    st=0
    while 1:
        ck=data.find('#cite_note-',st)
        if ck==-1:
            break
        else:
            st=data.find('[',ck)
            fi=data.find(']',st)
            data=data.replace(data[st:fi+1],'')

    return data


def eng_sentence(final_header_eng):

    start=-1
    finish=-1
    cnt=0


    # '('로 시작해서 ')'까지 찾아서 제거

    x=0
    while 1:
        if x==len(final_header_eng):
            break

        start=final_header_eng[x].find('(')
        if start==-1:
            x=x+1
            continue

        finish=final_header_eng[x].find(')',start)
        if finish==-1:
            tmp=final_header_eng[x][start:len(final_header_eng[x])+1]
        else:
            tmp=final_header_eng[x][start:finish+1]

        final_header_eng[x]=final_header_eng[x].replace(tmp,'')
        start=final_header_eng[x].find('(')

        if start==-1:
            x=x+1

        finish=-1

    # ~~~')'까지 찾아서 제거
    for x in range(len(final_header_eng)):

        finish=final_header_eng[x].find(')')
        if finish==-1:
            continue

        tmp=final_header_eng[x][:finish+1]
        final_header_eng[x]=final_header_eng[x].replace(tmp,'')
        finish=-1

    # 공백이거나 '.'만 있는 라인제거

    for x in range(len(final_header_eng)):

        if final_header_eng[cnt]=='' or final_header_eng[cnt]=='.':
            del final_header_eng[cnt]
        else:
            cnt=cnt+1

        if len(final_header_eng)-1==cnt:
            break



    return final_header_eng

def check_table_index(sources):

    #쓸때 없는 table 위치 찾기(kor)
    table_st=[]
    table_fi=[]
    st=-1
    fi=-1
    while 1:
        st=str(sources).find('<table',st+1)
        if st!=-1:
            table_st.append(st)
        else:
            break

    while 1:
        fi=str(sources).find('</table>',fi+1)
        if fi!=-1:
            table_fi.append(fi)
        else:
            break

    #table 쌍 맞춰서 리스트에 집어넣음
    table_set=[[] for i in range(len(table_fi))]
    i=0
    j=0
    while 1:

        if i>=len(table_fi):
            break
        ct=0
        while 1:
            if  j>=len(table_st) or table_fi[i]<table_st[j]:
                table_set[i].append(table_st[i])
                table_set[i].append(table_fi[j-1])
                break

            else:
                j=j+1
                ct=ct+1

        i=i+ct
    return table_set

def WeakTranslation(sourcesKOR_tmp,sourcesENG_tmp):

    start_k=str(sourcesKOR_tmp).find('<p>')
    start_e=str(sourcesENG_tmp).find('<p>')

    #문단이 없으면 다음 문서로 넘어가기
    if start_k==-1 or start_e==-1:
        return -1, -1

    finish_k=str(sourcesKOR_tmp).find('<h2>')
    finish_e=str(sourcesENG_tmp).find('<h2>')
    if finish_k==-1 or finish_e==-1:
        finish_k=0
        finish_e=0

    ########## KOREA ############
    tmp_k=str(sourcesKOR_tmp)[start_k:finish_k]
    tt=0
    while 1:

        idx=tmp_k.find('</p>',tt+1)
        if idx==-1:
            break
        else:
            tt=idx

    tmp_k=tmp_k[:tt]
    header_kor=remove_tags(tmp_k)
    header_kor=remove_comma(header_kor)
    header_kor=remove_bracket(header_kor)
    header_kor=remove_semantic(header_kor)
    header_kor=remove_brachet(header_kor)
    final_header_kor=kor_sentence.kor_sentence(header_kor)

    ########## ENGLISH ############
    tmp_e=str(sourcesENG_tmp)[start_e:finish_e]
    tt=0
    while 1:

        idx=tmp_e.find('</p>',tt+1)
        if idx==-1:
            break
        else:
            tt=idx

    tmp_e=tmp_e[:tt]
    header_eng=remove_tags(tmp_e)
    header_eng=remove_comma(header_eng)
    header_eng=remove_bracket(header_eng)
    header_eng=remove_semantic(header_eng)
    header_eng=remove_brachet(header_eng)
    final_header_eng=sent_tokenize(header_eng)
    final_header_eng=eng_sentence(final_header_eng)

    return final_header_kor, final_header_eng


def StrongTranslation(sourcesKOR_tmp, sourcesENG_tmp):

    #문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

    #문단이 없으면 다음 문서로 넘어가기
    if len(para_kor)==0 or len(para_eng)==0:
        return -1, -1

    ############# KOREA ############
    non_bmp_map=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    header_kor=remove_comma(str(para_kor).translate(non_bmp_map))
    header_kor=remove_bracket(header_kor)
    header_kor=remove_semantic(header_kor)
    header_kor=remove_tags(header_kor)
    if header_kor[len(header_kor)-2]==',':
        header_kor=header_kor[1:len(header_kor)-2]
    else:
        header_kor=header_kor[1:len(header_kor)-1]

    header_kor=remove_brachet(header_kor)
    final_header_kor=kor_sentence.kor_sentence(header_kor)

    ############# ENGLISH ############
    non_bmp_map2=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    header_eng=remove_comma(str(para_eng).translate(non_bmp_map))
    header_eng=remove_bracket(header_eng)
    header_eng=remove_semantic(header_eng)
    header_eng=remove_tags(header_eng)
    if header_eng[len(header_eng)-2]==',':
        header_eng=header_eng[1:len(header_eng)-2]
    else:
        header_eng=header_eng[1:len(header_eng)-1]
    header_eng=remove_brachet(header_eng)
    final_header_eng=sent_tokenize(header_eng)
    final_header_eng=eng_sentence(final_header_eng)

    return final_header_kor, final_header_eng

def header(sourcesKOR, sourcesENG, i, metric_result):



    #print ("[header] "+str(i))
    #쓸때 없는 table 부분 삭제
    tmp_kor=str(sourcesKOR)
    tmp_eng=str(sourcesENG)
    table_set_kor=check_table_index(sourcesKOR)
    table_set_eng=check_table_index(sourcesENG)


    #불필요한 table제거 (kor)
    kkk=[]
    for j in range(len(table_set_kor)):
        if table_set_kor[j]==[]:
            continue
        kkk.append(tmp_kor[table_set_kor[j][0]:table_set_kor[j][1]+9])

    for k in range(len(kkk)):
        tmp_kor=tmp_kor.replace(str(kkk[k]),'')

    #불필요한 table제거 (eng)
    eee=[]
    for l in range(len(table_set_eng)):
        if table_set_eng[l]==[]:
            continue
        eee.append(tmp_eng[table_set_eng[l][0]:table_set_eng[l][1]+9])

    for t in range(len(eee)):
        tmp_eng=tmp_eng.replace(str(eee[t]),'')


    sourcesKOR_tmp=BeautifulSoup(tmp_kor,"html.parser")
    sourcesENG_tmp=BeautifulSoup(tmp_eng,"html.parser")
    '''
    #강한번역, 약한번역에 따른 처리
    if metric_result>=0.8:
        final_header_kor, final_header_eng = StrongTranslation(sourcesKOR_tmp, sourcesENG_tmp)

    else:
        final_header_kor, final_header_eng = WeakTranslation(sourcesKOR_tmp, sourcesENG_tmp)
    '''
    final_header_kor, final_header_eng = WeakTranslation(sourcesKOR_tmp, sourcesENG_tmp)
    if final_header_kor==-1 or final_header_eng==-1:
        return -1

    #추출할 header를 저장하기 위한 파일오픈
    f_header_kor=open(header_path.format(lang='kor',idx=i),"w",encoding='UTF8')
    f_header_eng=open(header_path.format(lang='eng',idx=i),"w",encoding='UTF8')

    ###########  KOREA  ############
    for m in range(len(final_header_kor)):
                   f_header_kor.write(final_header_kor[m])
    f_header_kor.write("\n")

    ############  ENGLISH  ###########
    for x in range(len(final_header_eng)):
                f_header_eng.write(final_header_eng[x])
                f_header_eng.write("\n")
    f_header_eng.write("\n")


    f_header_kor.close()
    f_header_eng.close()

    return 0
