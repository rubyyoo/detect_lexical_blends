# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os.path
#from itertools import zip_longest
#from collections import defaultdict
#import jellyfish
from pyjarowinkler import distance
import time
#import gensim 
#from gensim.models import Word2Vec 
#import gensim.downloader as api

def evaluate(fanswer, fcands):

    with open(fanswer, 'r') as fanswer, open('input/candidates.txt', 'r') as fdata, open(fcands, 'r') as fcands:
        fanswer = fanswer.readlines()
        fcands = fcands.readlines()
        fdata = fdata.readlines()
        label=[]
        dataList=[]
        candList = []
        # take the first token
        
        for answer in fanswer:                                        
            label.append(answer.split()[0].strip())
            
        for d in fdata:       
            dataList.append(d.strip())
            
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        #tmpList=[]
        for cand in fcands:
            blend_cand = cand.split()[0].strip()
            candList.append(blend_cand)
            if blend_cand in label:
                tp += 1
            else:
                fp += 1
        
        for data in dataList:
            if data not in label and data not in candList:
                tn += 1
            elif data in label and data not in candList:
                fn += 1
                
        accuracy = (tp+tn)/(tp+fp+fn+tn)        
        precision= tp/len(candList)
        recall= tp/len(label)        
       

        print("accuracy\t{} ({}/{})".format(accuracy, tp+tn, tp+fp+fn+tn))
        print("precision\t{} ({}/{})".format(precision, tp, len(candList)))
        print("recall\t{} ({}/{})".format(recall, tp, len(label)))
    return 0

def process(output):    
    
    if  not os.path.isfile(output) :        
        with open(outputfile, 'w') as out, open('input/candidates.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts:
            dicts = dicts.readlines()
            cands = cands.readlines()
            cons = 'bcdfghjklmnpqrtvwxz'
            tmpstr = ''
            accepted = ['ght','lyn', 's', 'y', 'ch' ]

            for can in cands:                
                can = can.rstrip()
                if (len(can) > 15):
                   continue
                
                if (len(can)<= 2):                
                    continue
                
                if len(can) > 2:
                    count1, count2, count3 = 0
                    #count2 = 0
                    #count3 = 0
                    
                    if (can[0] in 'jkwyz' and can[0]== can[1]) or (can[-1] in 'vw' and can[-1]== can[-2]):
                            continue
                    for i, c in enumerate(can):        
                        
                        if can[i - 1] == can[i]:     
                            count1+=1
                        if i>=2 and can[i - 2] == can[i]:
                            count2+=1
                        if c in cons:                             
                            tmpstr += c
                            count3 +=1            
                        else:                    
                            count3 =0
                            tmpstr = ''
                            continue
                        
                    if count1>1 or count2>1 or (count3>2 and tmpstr not in accepted and tmpstr[-2:]!='ch' ) :                                           
                        continue                   
    
                fmt = "{}\n".format(can)
                #print("[writeToOutputFile]", fmt)
                out.write(fmt)
      
    return 0

def findSource():    
    fcands = 'output/fcands.txt'
    #model = api.load("glove-wiki-gigaword-100")
    #sim = model.similarity('million', 'cabbage')
    #print(sim)
    with open(fcands, 'w') as out, open('input/cands.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts:
        
        fdicts = dicts.readlines()
        cands = cands.readlines()
        tmpdicts = []
        for i in range(len(fdicts)):
            if i%1000==0:            
                tmpdicts.append(fdicts[i].rstrip())

       # tmpdicts.append('king')
        #tmpdicts.append('queen')
        
        dicts = {}        
        reversedicts = {}
        
        ### in case of preventing key error
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for letter in alphabet:
            dicts[letter] = []
        for letter in alphabet:
            reversedicts[letter] = []    
        ###    
        
        key = None
        reverseKey = None
        for line in tmpdicts:        
            
            #line1 = line.split()[1].strip()
            #line2 = line.split()[2].strip()
            #line = linetmp.split()[i+1].strip()

            line = line.strip()
            
            key = line[0] 
            reverseKey = line[-1] 
    
            if not line:
                key = None
                reverseKey = None
            elif not key or not key in dicts:
                dicts[key] = []
            if not reverseKey or not reverseKey in reversedicts: 
                reversedicts[reverseKey] = []            
                    
            dicts[key].append(line)   
            reversedicts[reverseKey].append(line[::-1])     
    
        #tmptmp
        for key in dicts:
            dicts[key].sort()
        
        for key in reversedicts:
            reversedicts[key].sort()
            

        prefixsim = 0
        suffixsim = 0
        #blend_cands=[]
        #cands = cands[:1000]
        #word_vectors = api.load("glove-wiki-gigaword-100")
        #model = gensim.models.Word2Vec(tmpdicts,min_count=1,size=32)        
        #model = gensim.models.Word2Vec([tmpdicts], min_count = 1, size = 100, window = 5)
        #similarity = model.similarity('king', 'queen') 
        #tmptmp
        #sorted(dicts, key=lambda x:x[1])
        for z, can in enumerate(cands):                
            can = can.strip()

            if z%900==0:
                print(can)
            
            if can == 'brunch':
                print()
            
            
            alpha = can[0]            
            reverseAlpha = can[-1]

            prefixsim=0
            suffixsim=0

            cand_list=[None] * (len(can)-1)
            
            #   for i, word in enumerate(s):

            for i in range(len(can)-1): 
                currCompPrefix = can[:i+1]
                currCompSuffix = can[i+1:][::-1]
                
                if currCompSuffix == 'hcnu':
                    print()
                
                idx_end_pref =-1
                idx_end_suf =-1
                idx_end_suf2 = -1
                
                ##for fast scan, set idx to find in dictionary
                idx_start_pref, low_param = search_startidx(dicts[alpha],currCompPrefix )
                if len(currCompPrefix) != 1:                    
                    idx_end_pref = search_endidx(dicts[alpha], currCompPrefix, low_param )
                
                idx_start_suf, low_param2 = search_startidx(reversedicts[reverseAlpha],currCompSuffix)
                if len(currCompSuffix) != 1:                
                    idx_end_suf = search_endidx(reversedicts[reverseAlpha],currCompSuffix , low_param2)
         
                ########test
                currCompSuffix2 = currCompSuffix[::-1]
                suffixPreAlpha = currCompSuffix2[0]
                
                idx_start_suf2, low_param3 = search_startidx(dicts[suffixPreAlpha],currCompSuffix2 )
                if len(currCompSuffix2) != 1:                    
                    idx_end_suf2 = search_endidx(dicts[suffixPreAlpha],currCompSuffix2, low_param3 )
                
                
                ########test
                cand_list[i] = [{'prefix':['',0], 'suffix':['',0]},0]

                for src1 in dicts[alpha][idx_start_pref:idx_end_pref]:
                    if src1 and src1.startswith(currCompPrefix): #if src1 and
                        prefixsim = distance.get_jaro_distance(can, src1,  winkler=True, scaling=0.07)           #can[:i+1],            
                        
                        if prefixsim>=0.6 and prefixsim<=0.85:                            

                            pref_history = cand_list[i][0]['prefix'][1]
                            suff_history = cand_list[i][0]['suffix'][1]
                            if (prefixsim+suff_history)>cand_list[i][1]:                                
                                cand_list[i][0]['prefix'][1] = prefixsim    #update prefix jw similarity     
                                cand_list[i][0]['prefix'][0] = src1         #update prefix str value 
                                cand_list[i][1] = suff_history+prefixsim + (0.1/((i+1)%(len(can)/2)+0.1)) #+(0.2/(i%(2/len(can))+0.1))    #else cand_list[i][1] #update sum
                                
                                if i == 0:
                                    break

                for src2 in reversedicts[reverseAlpha][idx_start_suf:idx_end_suf]:        
                    if src2 and src2.startswith(currCompSuffix[:len(currCompSuffix)-1]):  #if src2 and
                        suffixsim = distance.get_jaro_distance(can[::-1],src2,  winkler=True, scaling=0.09 )        #can[i+1:]                 

                        if suffixsim>=0.6 and suffixsim<=0.95:

                            pref_history = cand_list[i][0]['prefix'][1]
                            suff_history = cand_list[i][0]['suffix'][1]
                            if (suffixsim+pref_history)>cand_list[i][1]:
                                cand_list[i][0]['suffix'][1] = suffixsim  #else suff_history    #update prefix jw similarity      
                                cand_list[i][0]['suffix'][0] = src2         #update suffix str value 
                                cand_list[i][1] = pref_history+suffixsim + (0.1/((i+1)%(len(can)/2)+0.1)) #+ (0.2/(i%(2/len(can))+0.1))  #else cand_list[i][1] #update sum
                                
                                if i == len(can)-1:
                                    break
                            #@@@@prefix_cand[src1] = prefixsim
                        
                ####test this is for when sufix is located in the first part of the word
                for src3 in dicts[suffixPreAlpha][idx_start_suf2:idx_end_suf2]:
                    suffixsim2 = distance.get_jaro_distance(can, src3,  winkler=True, scaling=0.07)          #can[:i+1]              
                    
                    if suffixsim2>=0.6 and suffixsim2<=0.85:                            
                        ##########################
                        pref_history = cand_list[i][0]['prefix'][1]
                        suff_history = cand_list[i][0]['suffix'][1]
                        if (suffixsim2+pref_history)>cand_list[i][1]:                                
                            cand_list[i][0]['suffix'][1] = suffixsim2    #update prefix jw similarity     
                            cand_list[i][0]['suffix'][0] = src3        #update prefix str value 
                            cand_list[i][1] = pref_history+suffixsim2 + (0.1/((i+1)%(len(can)/2)+0.1)) #+ (0.2/(i%(2/len(can))+0.1))   #else cand_list[i][1] #update sum
                            
                            if i==0:
                                break
                            
                            
                    ######### data structure: list[0] = [dict (prefix1:[str,val],suf:[str,val]), sum]
            if cand_list[0][1]>0:        
                maxrow = max(cand_list, key=lambda x:x[1])
                prefstr = maxrow[0]['prefix'][0]
                suffstr = maxrow[0]['suffix'][0][::-1]
                preSim = maxrow[0]['prefix'][1]
                sufSim = maxrow[0]['suffix'][1]
                sum1 = maxrow[1]

                if prefstr and suffstr and (sum1>=1.4 and sum1<=1.9) :  
                    out.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(can, prefstr, suffstr, preSim, sufSim, sum1))

def jarowinkler(can,dic):
  
    s= ''
    l= ''
    m = 0
    pf=0
    trans=0
    simw=0
    winsize = 0
        
    if len(can)>len(dic):
        s = dic
        l =can 
    else:
        s = can
        l =dic

    winsize= int(max((len(l)/2)-1, 0))
    for i, word in enumerate(s):                
        if s[i] == l[i]:
            m+=1
            if i<4:
                pf+=1
                
        start = max(i-winsize, 0)
        end = min(i+winsize, len(l))
        for j in range(start, end):
            if(i==j and s[i] == l[i]):
                continue                        
            if s[i] == l[j]:
                trans+=1;
                break;
               
    if(m!=0):
        trans = trans/2
        simj = 1/3 * (m/len(l) + m/len(s) + (m-trans)/m)
        simw = simj + pf*0.1*(1- simj)

    return simw


def search_startidx(input, key):
   low = 0
   high = len(input)-1
   tmpLow = -1
   while low <= high:
      mid = int((low + high)/2)
      if input[mid] >= key:
      #if input[mid].startswith(key):          
         if mid ==0:
             tmpLow = tmpLow if input[tmpLow].startswith(key) else mid 
             return (mid, tmpLow)
         if tmpLow == -1:
             tmpLow = mid
         if input[mid] >= key and input[mid-1] < key:
             tmpLow = tmpLow if input[tmpLow].startswith(key) else mid 
             return (mid, tmpLow)
         else:              
             high = mid - 1    
      else:            
         low = mid + 1
   return (-1,-1)

def search_endidx(input, key, lowidx):
   low = lowidx
   high = len(input)-1
   
   while low <= high:
      mid = int((low + high)/2)
      if mid==len(input)-1:
          return mid
      if input[mid].startswith(key):     
         if mid ==0:
             return mid
         if not input[mid+1].startswith(key):
             return mid
         else: 
             low = mid + 1    
      else:
         high = mid - 1
   return -1   
            
if __name__ == "__main__":
    
    start = time.time()

    outputfile = 'input/cands.txt'
    #process(outputfile)    
    findSource()    
    answer = 'label/blends.txt' 
    cands = 'output/fcands.txt' 
    evaluate(answer, cands)
    #d = distance.get_jaro_distance("brunch","actinobranch",  winkler=True, scaling=0.07)  
    #print(d)
    #model = gensim.models.Word2Vec(tmpdicts, min_count = 1, size = 100, window = 5)
    end = time.time() 
    print(end - start)
    #model.similarity('casual', 'memo')