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

class BM_model:
    def __init__(self):
        self.N_document = 0
        self.sum_length = 0
        self.word_to_count = {}

    def rm_pun(self,sencen):
        sen = sencen.strip()
        return re.sub('[+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+', ' ', sen)
    def process_sentence(self,sentence):
        if 'question:' in sentence:
            return sentence[9:], 0
        elif 'answer:' in sentence:
            return sentence[7:], 1
        else:
            return None
    def init_model(self,source_path):
        f = open(source_path, mode='r', encoding='utf-8')
        for line in f.readlines():
            sentence = self.process_sentence(line)
            if sentence and sentence[1] ==0:
                sen = sentence[0]
                sen = self.rm_pun(sen)
                sen = jieba.cut(sen)
                sen = ' '.join(sen)
                words = sen.split()
                self.sum_length += len(words)
                self.N_document += 1
                for word in words:
                    if word not in self.word_to_count:
                        self.word_to_count[word] = 1
                    else:
                        self.word_to_count[word] += 1
        f.close()
    def save_model(self,model_path):
        f = open(model_path,mode = 'w',encoding = 'utf-8')
        f.write('N_document '+str(self.N_document)+'\n')
        f.write('sum_length ' + str(self.sum_length) + '\n')
        for key in self.word_to_count:
            value = self.word_to_count[key]
            f.write(key+' '+str(value)+'\n')
        f.close()
    def load_model(self,model_path):
        f = open(model_path,mode = 'r',encoding = 'utf-8')
        for line in f.readlines():
            key,value = line.split()
            value = value.strip('\n')
            if key == 'N_document':
                self.N_document = int(value)
            elif key =='sum_length':
                self.sum_length = int(value)
            else:
                self.word_to_count[key] = int(value)
        f.close()

    def cal_K(self,dl, k1=2, b=0.75):
        avg_dl = self.sum_length/self.N_document
        return k1 * (1 - b + b * (dl / avg_dl))

    def cal_R(self,qi, d):
        words = d.split()
        fi = words.count(qi)
        dl = len(words)
        K = self.cal_K(dl)
        k1 = 2
        return fi * (k1 + 1) / (fi + K)

    def IDF(self, word):
        # N = id_count['whole_sum_ount_len']
        nw = self.word_to_count.get(word, 0)
        up = self.N_document - nw + 0.5
        bottom = nw + 0.5
        return math.log(up / bottom)

    def score(self,Q, d):
        Q_words = Q.split()
        score = 0
        for q_word in Q_words:
            wi = self.IDF(q_word)
            score = score + wi * self.cal_R(q_word, d)
        return score
def test(source_path):
    f = open(source_path,mode = 'r',encoding = 'utf-8')
    index = 0
    Questions = []
    for line in f.readlines():
        if 'question:' in line and index <10:
            Questions.append(line[9:])
    f.close()
    return Questions
def ps(sentence):
    line = jieba.cut(sentence)
    return ' '.join(line)
if __name__=='__main__':
    source_path = '/home/yueshifeng/repos/xiaoqi/retrieval_based/data/test.txt'
    model_path = 'model.txt'
    bm = BM_model()
    #bm.init_model(source_path)
    #bm.save_model(model_path)
    bm.load_model(model_path)
    questions = test(source_path)
    Q = '订大陆飞台湾的机票需要什么证'
    Q = ps(Q)
    for q in questions:
        line = ps(q)
        print(q,bm.score(Q,line))
