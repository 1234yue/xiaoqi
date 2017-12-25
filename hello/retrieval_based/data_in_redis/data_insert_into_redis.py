# -*- coding: utf-8 -*-
import io
import redis
import jieba
import gzip
import os
import sys
import re
import tarfile
import fileinput



def insert_set_into_redis(r, key, value):
    for v in value:
        r.sadd(key, v)


def insert_in_to_redis(key, value, r):
    r.set(key, value)


def all_in_redis(source_path):
    f = open(source_path, mode="r", encoding="utf-8")
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    index = 0
    q = True
    for line in f.readlines():
        key = ''
        if q:
            key = 'Q_' + str(index)
        else:
            key = 'A_' + str(index)
            index = index + 1
        insert_in_to_redis(key, line, r)
        q = not q
    f.close()


def build_inverted_index_for_QA(source_path):
    f = open(source_path, mode="r", encoding="utf-8")
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    q = True
    index = 0
    for line in f.readlines():
        if q:
            words = line.split()
            for word in words:
                if 'Q_' not in word and 'A_' not in word:
                    r.sadd(word, index)
        else:
            index = index + 1
        q = not q
    f.close()


def rm_pun(sencen):
    sen = sencen.strip()
    return re.sub('[+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+', ' ', sen)

def build_inverted_index_for_synonyms(source_path):
    f = open(source_path,mode = 'r',encoding = 'utf-8')
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    index = 0
    for line in f.readlines():
        index = index + 1
        key , value = line.split(':')
        values = value.split()
        values.append(key)
        for v in values:
            k = 'synonyms_id_to_word'+str(index)# index:word1 word2
            r.sadd(k,v)
            vw = 'synonyms_word_to_id|'+v       #{word:id}
            r.sadd(vw,index)
    f.close()
def build_inverted_index(yuliao_path,dict_path = None):
    all_in_redis(yuliao_path)
    print('begin build yuliao')
    build_inverted_index_for_QA(yuliao_path)
    print('begin build index')
    if dict_path:
        build_inverted_index_for_synonyms(dict_path)
    print('data is ok')

if __name__ == '__main__':

    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    pre = '/home/yueshifeng/repos/xiaoqi/retrieval_based/data'
    source_path = os.path.join(pre,'yuliao.txt')
    build_inverted_index(source_path)


