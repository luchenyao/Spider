# coding=utf-8

import json
import re


def json_to_dict(filepath):
    with open(filepath,'rb') as f:
        corpus=f.readlines()
        law_str=""
        for line in corpus:
            line=line.decode('utf-8')
            law_str=law_str+line
        raw_dict=json.loads(law_str)
        print(type(raw_dict))
        return raw_dict


def dict_clean(raw_dict):
    if(isinstance(raw_dict,dict)):
        for i in range(len(raw_dict)):
            temp_key=raw_dict.keys()[i]
            temp_value=raw_dict[temp_key]
            print("%s:%s" % (temp_key, temp_value))
            dict_clean(temp_value)


path="./posts.json"

data=json_to_dict(path)
dict_clean(data)



