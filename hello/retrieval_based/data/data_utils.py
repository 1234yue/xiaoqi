import io
import redis
import jieba
import gzip
import os
import sys
import re
import tarfile
import fileinput

def rm_pun(sencen):
    sen = sencen.strip()
    return re.sub('[+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+', ' ', sen)


def process_sentence(sentence):
    if 'question:' in sentence:
        return sentence[9:], 0
    elif 'answer:' in sentence:
        return sentence[7:], 1
    else:
        return None

def process_data(source_path,target_path):
    f = open(source_path,mode = 'r',encoding = 'utf-8')
    fw = open(target_path,mode = 'w',encoding = 'utf-8')
    for line in f.readlines():
        sentence = process_sentence(line)
        if sentence:
            if sentence[1] ==1:
                fw.write(sentence[0].strip('\n')+'\n')
            else:
                sen = rm_pun(sentence[0]).strip('\n')
                words = jieba.cut(sen)
                senten = ' '.join(words)
                fw.write(senten+'\n')
    fw.close()
    f.close()
if __name__=='__main__':
     source_path = 'mafengwo.txt'
     target_path = 'yuliao.txt'
     process_data(source_path, target_path)
     print('data is ok')