#!/usr/bin/python3
import random
import os,sys,signal
import json

N=8#number of word displaying once
S=2#number of times of a word to regard as learned
T=4#timeout in sec in testing mode
t=1.8#timeout in sec in revising mode

log=open('test.log','a')
learned=[]
            
class map():#governs all imported data
    
    def __init__(self,dict=open('words.json'),mode='t',N=8):
        self.data=json.load(dict)
        self.mode=mode
        self.__keys=list(self.data)
        self.N=N
    
    def proc(self,corr='corr.json',final='final.json'):
        if os.path.isfile(corr):
            self.correct=json.load(open(corr))
        else:self.correct={}
        if self.mode=='t':
            final=set()
            for word in self.correct:
                if self.correct[word]>=S:
                    final.add(word)
            final=list(final)
            json.dump(final,open('final.json','w'))
        elif 'r' in self.mode:
            if os.path.isfile(final):
                final=json.load(open(final))
                for word in list(DICT):
                    if word not in final:del DICT[word]
            else:print('No record found! Cannot review.')
        elif self.mode=='l' and final:
            FINAL=json.load(final)
            for word in FINAL:
                if word in DICT:del DICT[word]

    def popfromdict(self):
        A,B=[],[]
        if self.N>len(self.__keys):self.N=len(self.__keys)
        for i in range(self.N):
            word=random.choice(self.__keys)
            A.append(word)
            B.append(self.data[word])
            self.__keys.remove(word)
        random.shuffle(A)
        return A,B
    
    def __len__(self):
        return len(self.__keys)
    
    def listget(self,list):
        out=[]
        for i in list:
            out.append(self.data[i])
        return out

class TMOException(Exception):
    pass

def alarmHandler(signum, frame):
    raise TMOException

class test():
    
    def __init__(self,ref=None,T=4):
        self.ref=ref
        self.tmoT=T
        self.__flush()
        
    def prep(self):
        self.__A,self.__B=self.ref.popfromdict()
        print(','.join(self.__A)+',',
              file=log,end='',flush=True)
        os.fsync(log)
        self.__B.sort(key=lambda x:x[-1])
        os.system('clear')
    
    def Input(self,word):
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.alarm(self.tmoT)
        try:
            ans = input(word+' ')
            signal.alarm(0)
            if ans.isdigit():
                ans=int(ans)
                self.ansc+=1
                if self.__B[ans]==self.ref.data[word]:
                    self.corrc+=1
                    if word in self.ref.correct:
                        self.ref.correct[word]+=1
                    else:self.ref.correct[word]=1
                    learned.append(word)
                else:self.__err.append(word)
            else:
                self.__err.append(word)
        except TMOException:
            print(' time over',end='')
            self.__err.append(word)
            input()
        #signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return
    
    
    def __flush(self):
        self.__corr,self.__err,self.__ans=[],[],[]
        self.ansc,self.corrc=0,0
        
    def dump(self):
        if self.ref.mode=='r+':
            for i in self.__err:
                if i in self.ref.correct:
                    if self.ref.correct[i]>=1:
                        self.ref.correct[i]-=1
                    else:
                        del self.ref.correct[i]
        print ('###SAVING DATA###')
        json.dump(self.ref.correct,open('corr.json','w'))
    
    def print(self):#governs all things after answer before saving
        self.__err.sort(key=len)
        err_out=[str.ljust(len(self.__err[-1])) for str in self.__err]
        print('Mistakes:')
        for i in range(len(self.__err)):
            print(err_out[i]+'\t'+''.join(self.ref.data[self.__err[i]]))
        print('totally {!s}'.format(len(self.__err)))
        if self.ansc==self.corrc:
            print('all answered correct')
        else:
            print('not all answered correct')
        print(len(self.ref))
        self.__flush()
        input('press enter to continue')
        
    def quest(self):
        
        for i in range(self.ref.N):
            print('{}'.format(i)+'\t'+self.__B[i][-1])
        input('press enter to start')
        
        for i in range(self.ref.N):
            self.__ans.append(self.Input(self.__A[i]))
        
def learn(DICT,num):
    
    A,B=[],[]
    keys=list(DICT)
    for i in range(N):
        word=random.choice(keys)
        A.append(word)
        B.append(DICT[word])
        keys.remove(word)
    A.sort(key=len)
    A_out=[word.ljust(len(A[-1])) for word in A]
    for i in range(N):print(A_out[i]+'\t'+''.join(DICT[A[i]]))
    learned.extend(A)
    P=input('Test now? y/n ')
    if P=='y':
        D={}
        for word in learned:
            D[word]=DICT[word]
        test(D,N)
        return
    learn(DICT,num)

DICT=map()
DICT.proc()
Test=test(ref=DICT)
while True:
    Test.prep()
    Test.quest()
    Test.dump()
    Test.print()
'''
if mode!='l':
    imp(mode,DICT)
elif os.path.isfile('final.json'):
    imp(mode,DICT,final=open('final.json'))
else:
    imp(mode,DICT)

if mode=='t' or mode=='r':
    test(DICT,N)
elif mode=='l':
    os.system('clear')
    learn(DICT,input('how many? '))
'''
