import io
import redis
import jieba
import gzip
import os
import sys
import re
import tarfile
import fileinput
# bing cha ji
def find_list(x,f):
    a=[]
    while x != f[x]:
        a.append(f[x])
        x = f[x]
    return a


def find(x,f):
    if f[x]==x:
      return x
    else:
      f[x] = find(f[x],f)
      return f[x]
def union(l,r,f):
    L = find(l,f)
    R = find(r,f)
    if(L!=R):
        f[L]=R
def get_word_id(source_path):
    f = open(source_path,mode = 'r',encoding = 'utf-8')
    index = 0
    word_id={}
    for line in f.readlines():
        key,values = line.split('->')
        key = key.strip()
        if key not in word_id:
            word_id[key]=index
            index = index + 1
        values =values.split()
        for value in values:
            v = value.split('[')[0]
            if v not in word_id:
                word_id[v] = index
                index = index + 1
    f.close()
    id_word={}
    for key in word_id:
        v = word_id[key]
        id_word[v]=key
    return word_id,id_word
def process(source_path,target_path):
    word_id,id_word= get_word_id(source_path)
    w_len = len(word_id)
    fa=[]
    for i in range(w_len):
        fa.append(i)
    for i in range(len(fa)):
        if i!=fa[i]:
            print('wrong')
    f = open(source_path, mode='r', encoding='utf-8')
    for line in f.readlines():
        key,values = line.split('->')
        key = key.strip()
        l=int(word_id[key])
        values = values.split()
        for value in values:
            v = value.split('[')[0]
            r = int(word_id[v])
            #print(l,r,type(l),type(r))
            union(l,r,fa)
    index = 0
    id_words={}
    for i in range(w_len):
        key = find(i,fa)
        if key not in id_words:
            id_words[key]=[]
        id_words[key].append(i)
    fw = open(target_path,mode = 'w',encoding='utf-8')
    for key in id_words:
        for v in id_words[key]:
            word = id_word[v]
            fw.write(word+find_list(v)+' ')
        fw.write('\n')
    fw.close()
    f.close()

def process_one(source_path,target_path):
    key_word = {}
    f = open(source_path, mode='r', encoding='utf-8')
    for line in f.readlines():
        key,values = line.split('->')
        key = key.strip()
        if key not in key_word:
            key_word[key] = []
        values = values.split()
        for value in values:
            key_word[key].append(value.split('[')[0])
    fw = open(target_path,mode = 'w',encoding='utf-8')
    for key in key_word:
        fw.write(key+' ')
        vs = list(set(key_word[key]))
        for v in vs:
            word = v
            fw.write(word+' ')
        fw.write('\n')
    fw.close()
    f.close()

if __name__=='__main__':
    source_path='syms.txt'
    target_path='/home/yueshifeng/repos/xiaoqi/new.txt'
    process_one(source_path,target_path)#we just quchong now
    print('tongyici quchong is ok')