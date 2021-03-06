
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy
import kor_sentence


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
    header_kor = header_kor[:len(header_kor) - 4]
    final_header_kor = kor_sentence.kor_sentence(header_kor)


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
    final_header_eng = sent_tokenize(header_eng)
    final_header_eng = eng_sentence(final_header_eng)


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
    #header_kor=remove_brachet(header_kor)
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
    #header_eng=remove_brachet(header_eng)
    final_header_eng=sent_tokenize(header_eng)
    final_header_eng=eng_sentence(final_header_eng)

    return final_header_kor, final_header_eng

def header_for_link(sourcesKOR, sourcesENG, i, metric_result ):
    #print("[header_for_link] " + str(i))
    # 쓸때 없는 table 부분 삭제
    tmp_kor = str(sourcesKOR)
    tmp_eng = str(sourcesENG)
    table_set_kor = check_table_index(sourcesKOR)
    table_set_eng = check_table_index(sourcesENG)

    # 불필요한 table제거 (kor)
    kkk = []
    for j in range(len(table_set_kor)):
        if table_set_kor[j] == []:
            continue
        kkk.append(tmp_kor[table_set_kor[j][0]:table_set_kor[j][1] + 9])

    for j in range(len(kkk)):
        tmp_kor = tmp_kor.replace(str(kkk[j]), '')

    # 불필요한 table제거 (eng)
    eee = []
    for j in range(len(table_set_eng)):
        if table_set_eng[j] == []:
            continue
        eee.append(tmp_eng[table_set_eng[j][0]:table_set_eng[j][1] + 9])

    for j in range(len(eee)):
        tmp_eng = tmp_eng.replace(str(eee[j]), '')

    sourcesKOR_tmp = BeautifulSoup(tmp_kor, "html.parser")
    sourcesENG_tmp = BeautifulSoup(tmp_eng, "html.parser")

    # 문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

    '''
    #강한번역, 약한번역에 따른 처리
    if metric_result>=0.8:
        final_header_kor, final_header_eng = StrongTranslation(sourcesKOR_tmp, sourcesENG_tmp)

    else:
        final_header_kor, final_header_eng = WeakTranslation(sourcesKOR_tmp, sourcesENG_tmp)
    '''
    final_header_kor, final_header_eng = WeakTranslation(sourcesKOR_tmp, sourcesENG_tmp)
    if final_header_kor==-1 or final_header_eng==-1:
        return -1, -1

    ###########  KOREA   ###########
    tmp_kor_link = [[] for j in range(len(final_header_kor))]

    # <a ~ </a>부분 잘라내기
    for m in range(len(final_header_kor)):
        start = 0
        finish = 0
        while 1:
            start = final_header_kor[m].find('<a')
            if start != -1:
                finish = final_header_kor[m].find('</a>')
                tmp_kor_link[m].append(final_header_kor[m][start:finish + 4])
            else:
                break

            while 1:
                start = final_header_kor[m].find('<a', start + 1)
                if start != -1:
                    finish = final_header_kor[m].find('</a>', finish + 1)
                    tmp_kor_link[m].append(final_header_kor[m][start:finish + 4])
                else:
                    break
            break

    # <a ~ </a>부분에서 단어만 추출
    tmp = [[] for j in range(len(tmp_kor_link))]
    k_link_list = [[] for j in range(len(tmp_kor_link))]
    for k in range(len(tmp_kor_link)):
        if len(tmp_kor_link[k]) == 0:
            continue
        for j in range(len(tmp_kor_link[k])):
            # title 부분
            st = tmp_kor_link[k][j].find('title="')
            if st == -1:
                continue
            fi = tmp_kor_link[k][j].find('"', st + 7)
            tt = tmp_kor_link[k][j]

            if str(tt[fi - 1]) == ' ':
                tt = tt[st + 7:fi - 1]
            else:
                tt = tt[st + 7:fi]

            kk = tt.find(':')
            if kk >= 0:
                tt = tt[kk + 1:]
            k_link_list[k].append(str(tt))


    ###########  ENGLISH  ###########
    tmp_eng_link = [[] for j in range(len(final_header_eng))]
    # <a ~ </a>부분 잘라내기
    for m in range(len(final_header_eng)):
        start = 0
        finish = 0
        while 1:
            start = final_header_eng[m].find('<a')
            if start != -1:
                finish = final_header_eng[m].find('</a>')
                tmp_eng_link[m].append(final_header_eng[m][start:finish + 4])
            else:
                break

            while 1:
                start = final_header_eng[m].find('<a', start + 1)
                if start != -1:
                    finish = final_header_eng[m].find('</a>', finish + 1)
                    tmp_eng_link[m].append(final_header_eng[m][start:finish + 4])
                else:
                    break
            break

    # <a ~ </a>부분에서 단어만 추출
    tmp = [[] for j in range(len(tmp_eng_link))]
    e_link_list = [[] for j in range(len(tmp_eng_link))]
    for k in range(len(tmp_eng_link)):
        if len(tmp_eng_link[k]) == 0:
            continue
        for j in range(len(tmp_eng_link[k])):
            # title 부분
            st = tmp_eng_link[k][j].find('title="')
            if st == -1:
                continue
            fi = tmp_eng_link[k][j].find('"', st + 7)
            tt = tmp_eng_link[k][j]

            if str(tt[fi - 1]) == ' ':
                tt = tt[st + 7:fi - 1]
            else:
                tt = tt[st + 7:fi]

            kk = tt.find(':')
            if kk >= 0:
                tt = tt[kk + 1:]
            e_link_list[k].append(str(tt))

    return (k_link_list, e_link_list)
