import urllib.request, urllib.error
import time,random
import os
import codecs,sys,json

def reqgen(word):
    url='http://dict.youdao.com/search?q='+word
    return url

def find(req):
    global code
    code=urllib.request.urlopen(req)
    code=code.read()
    
    pos_s=code.find(b'<ul>')+4
    pos_e=code.find(b'</ul>',pos_s)
    raw_meaning=code[pos_s:pos_e].splitlines()
    meaning=[codecs.decode(m) for m in raw_meaning if m]
    meaning=[x[9:-5] for x in meaning]
    pos_so=code.find(b'<span class="phonetic">')+23
    pos_s=code.find(b'<span class="phonetic">',pos_so)+23
    if pos_s==22:
        pos_s=pos_so
    pos_e=code.find(b'</span>',pos_s)
    phoenetic=codecs.decode(code[pos_s:pos_e])
    return meaning,phoenetic

raw_wordlist=open('wordlist.txt')
#new_wordlist=open('newlist.txt','a')
DICT=json.load(open('words.json'))

#for word in raw_wordlist:
while True:
    #word=word.rstrip(' \n')
    word=input('word ')
    if word and word not in DICT:
        req=reqgen(word)
        meaning,phoenetic=find(req)
        meaning=[_m for _m in meaning if word.capitalize() not in _m and '[' not in _m]
        meaning_out=','.join(meaning)
        while 'href' in meaning_out:
            print('Requested {} not found!'.format(word))
            word=input('New word:')
            req=reqgen(word)
            meaning,phoenetic=find(req)
            meaning=[_m for _m in meaning if word.capitalize() not in _m and '[' not in _m]
            meaning_out=','.join(meaning)
        meaning_out=meaning_out.rstrip(',')
        out=[phoenetic,meaning_out]
        print(word)
        DICT[word]=out
        json.dump(DICT,open('words.json','w'))
    elif word in DICT:
        print('already in DICT')
