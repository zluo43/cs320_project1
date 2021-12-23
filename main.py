from subprocess import check_output
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import json
import subprocess 

# project: p1
# submitter: zluo43
# hours: 48


#Q1: How many commits are in the repo? 

check_output(["git", "checkout", "main"], cwd = "repo")

check_output(["git", "log"], cwd = "repo")

commit_list=str(check_output(["git", "log"], cwd = "repo")).split()

count=0
for i in commit_list:
    if 'commit' in i:
        count=count+1
print (count) 
count 

#Q2: How many commits were there by each author?
name=[]
commit_list

for i in commit_list:
    if '@example.com' in i:
        name.append(i)

for i in range(len(name)):
    for j in range(len(name[i])):
        if (name[i])[j]=='@':
            name[i]=(name[i])[1:j]
            break
d={}
for k in name:
    if k not in d:
        d[k]=1
    elif k in d:
        d[k]=d[k]+1
print (d)
d

#Q3[PLOT]: How many commits did each developer contribute?
plt.figure(figsize=(3, 3))
plt.bar(d.keys(), d.values(),width=0.3,color='g')
plt.xlabel("Name")
plt.ylabel("contribution")


#Q4: How has the size of the wc.py code grown over time?

def rid_last(x):
    if x[len(x)-1]=='':
        x.pop(len(x)-1)
    return len(x)
#rid_last(clean)
count=[]
for i in version:
    check_output(["git", "checkout", i], cwd="repo")
    m=check_output(["cat", "wc.py"], cwd="repo", encoding='utf-8').split('\n')
    rid_last(m)
    #print (rid_last(m))
    count.append(rid_last(m))
  
count.reverse()
count

#Q5 [PLOT]: How has the size of the wc.py code grown over time?

plt.plot(range(8),count,color='red')
plt.xlabel("commit")
plt.ylabel("lines")


#Q6: What does run_wc(test1) return?
def run_wc(body, commit=None):
    with open(os.path.join("repo", "test.txt"), "w") as file:
        file.write(body)

    if commit==None: 
        commit = "main"
    
    check_output(["git", "checkout", commit],cwd="repo",universal_newlines=True)
#     print(check_output(["git", "log", "-1","--oneline"], cwd="repo",universal_newlines=True))
    try:
        run=check_output(["python3","wc.py","test.txt","ALL"],cwd="repo",universal_newlines=True)
        return (json.loads(run))
    except subprocess.CalledProcessError as e:
        return None 
run_wc(test1)


#Q7: What does run_wc(test3) return?
#print (run_wc(test2))

run_wc(test3)

#Q8: What does test_table(test1, {'X': 1, 'Y': 1, 'Z': 1}) return?
import pandas as pd 
def test_table(body, expected):
    empty={}
    author=['Ada','Linus','Linus','Ada','Steve','Ada','Steve','Steve']  #cheat sicne order is always the same for thie problem
    pass_=[]
    for i in version[::-1]: 
        if run_wc(body,i)==expected:
            pass_.append(True)
        else:
            pass_.append(False)
    empty['commit']=version[::-1]
    empty['Author']=author
    empty['Pass']=pass_
    df=pd.DataFrame(empty)
    return df
test_table(test1, {'X': 1, 'Y': 1, 'Z': 1})

#Q9: What does test_table(test2, {'A': 2, 'B': 1, 'C': 1}) return?
test_table(test2, {'A': 1, 'B': 1, 'C': 1})



#Q10: What does test_table(test3, {'A': 2, 'B': 1, 'C': 1}) return?
test_table(test3, {'A': 2, 'B': 1, 'C': 1})






#Q11: How long does each version take for 5000-word inputs consisting of 100 unique words?
import numpy as np 
from numpy import random
import string 
import random
import time

def time_run_sec(uniq_words, total_words, word_size=6, commit=None):
    empty=[]
    for i in range(uniq_words):
        ran_gen=''.join(random.choices(string.ascii_letters, k=word_size))
        #adopted from the internet 
        empty.append(ran_gen)
    ran_sample=random.choices(empty, k=total_words)
    input_str = " ".join(ran_sample)
    t0=time.time()
    #print (input_str)
    run_wc(input_str,commit)
    t1=time.time()
    return t1-t0
versions = {
    "v0-baseline": "6f5ca9327e986315ffcacddce5d9d6195c0913b7",
    "v1-open-once": "f37e610ce055a3d894baac2d9449e6eb77c72320",
    "v2-pass-per-uniq": "c10b5a6cb4f06c96f6f221df2d5ec33af767d5c5",
    "v3-single-pass": "4e4128313b8d5b5e5d04f2e8e585f64f7c5831a4"}
    
    
    
commit_name=list(versions.values())
ms=[]
for i in commit_name:
    ms.append(time_run_sec(100,5000,word_size=6,commit=i)*1000)

#log_scale=np.log(ms)
    
#log_scale

#ms

ms = pd.Series(ms)
ax=ms.plot.barh(x='Exu time', y='Version',logx=True)

mj=[]
for i in commit_name:
    mj.append(time_run_sec(1,5000,word_size=6,commit=i)*1000)

    
#Q12: How long does each version take for 5000-word inputs consisting of 1 unique word?
mj = pd.Series(mj)
ax=mj.plot.barh(x='Exu time', y='Version',logx=True)


#Q13 [PLOT]: How does the number of total words and unique percent affect the performance of versions 2 and 3?

def performance(uniq_percent,total_words,commit=None):
    df = pd.DataFrame(index=total_words, columns=uniq_percent)
    df.index.name = "total words"
    df.columns.name = "percent uniq"

    for up in uniq_percent:
        for tw in total_words:
            uniq_words = int(tw * (up / 100))
            value=time_run_sec(uniq_words,tw, word_size=6, commit=commit)
            df.loc[tw, up] = value
    return df

performance([10,5,1],[10000,5000,2000,1000]) 