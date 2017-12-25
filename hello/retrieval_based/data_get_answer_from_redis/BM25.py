import io
import redis
import jieba
import gzip
import os
import sys
import re
import tarfile
import fileinput
import math
import redis
def save_three_number(x):
    return float(int(x*1000)/1000)

def log(x):
    return math.log(x)

def log_di(x,y):
    return math.log(x)/math.log(y)

def count_word(source_path):
    f = open(source_path,mode = 'r',encoding='utf-8')
    id_count ={}
    d_sum_len = 0
    count = 0
    is_q = True
    try:
        for line in f.readlines():
            if is_q:
                is_q = False
            else:
                is_q = True
                continue
            words = line.strip().split()
            count = count + 1
            d_sum_len = d_sum_len + len(words)
            for word in words:
                if word in id_count:
                    id_count[word] = id_count[word] + 1
                else:
                    id_count[word] = 1
        return id_count,count,d_sum_len
    except:
        print('something wrong in cal idf')
    f.close()

def test(source_path):
    cidian,count,d_sum_len = count_word(source_path)
    '''
    test = '据说 毛主席纪念堂 自 今年 3 月 1 日 开始 到 8 月 31 日 进行 闭馆 整修   期间 不 接待 瞻仰   请问 这是 真的 吗'
    test = test.split()
    for word in test:
        print(IDF(cidian, word),cidian.get(word,0),word)
    '''
    #r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    f = open(source_path,mode = 'r',encoding ='utf-8')
    index = 0
    Q = '东北师范大学 属于 长春市 哪个 区'
    for line in f.readlines():
        index = index + 1
        if index >10:break
        s = score(Q,line,cidian,count,d_sum_len)
        print(s,line)
    f.close()

#calculate R(q,d)
def cal_K(dl , avg_dl,k1 =2,b =0.75):
    return k1*(1-b+b*(dl/avg_dl))

def cal_R(qi,d,avg_dl):
    words = d.split()
    fi = words.count(qi)
    dl = len(words)
    K = cal_K(dl,avg_dl)
    k1 = 2
    return fi*(k1+1)/(fi+K)

def save(source_path,target_path):
    id_count, count, d_sum_len = count_word(source_path)
    fw = open(target_path,mode = 'w',encoding='utf-8')
    #id_count, count =100,305
    fw.write('N_document: '+str(count)+'\n')
    fw.write('sum_length: '+str(count)+'\n')
    for key in id_count:
        fw.write(key+':'+str(id_count[key])+'\n')
    fw.close()
if __name__ == '__main__':
    pre = '/data/repos_ysf/rm_tongyici/data/'
    source_path = pre+'yuliao.txt'
    target_path = pre+'BM_SAVE.txt'
    test_path = pre + 'test.txt'
    #save(source_path,target_path)
    test(test_path)
    print('save is ok')