import io
import redis
import jieba
import gzip
import os
import sys
import re
import tarfile
import fileinput

class synonmy_model:
    def __init__(self):
        self.word_to_id = {}
        self.id_to_words = {}
    def load_model(self,source_path):
        index = 0
        f = open(source_path,mode = 'r',encoding = 'utf-8')
        for line in f.readlines():
            index = index + 1
            words = line.strip('\n').split()
            self.id_to_words[index] = []
            for word in words:
                self.word_to_id[word] = index
                self.id_to_words[index].append(word)
        f.close()
    def find_synonmy(self,word):
        if word in self.word_to_id:
            index = self.word_to_id[word]
            return self.id_to_words[index]
        return None