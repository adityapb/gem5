import sys
import re
import math
import matplotlib.pyplot as plt

import seaborn as sns

p=64
limit = 4
limit_2 = 4
# import matplotlib.pyplot as plt
# file_path = 'ep_128_l2.txt'
# tag = 'tag_ep_128'
# file_path = 'lu.128.l2.m5out/a.out'
# tag = 'tag_lu_128'
file_path ='lu_64_l2.txt'
tag ='tag_lu_64'
# file_path = 'ep_64_l2.txt'
# tag = 'tag_ep_64'
# file_path ='cg_64_l2.txt'
# tag ='tag_cg_64'
import os
if(1):
    if(os.path.exists('aaa/')==0):
        os.system('mkdir aaa')
    os.system('rm -rf aaa/*txt')

def my_set(x):
    return set(x)

def percentile_plot(data,x,y,t):
    x_ = [kk*100/(len(data)) for kk in (range(len(data)))]
    # plt.plot(x_,sorted(data),label=message)
    # sb.scatterplot(x=x_,y=sorted(data))
    sns.set_style("darkgrid")
    sns.lineplot(x=x_, y=sorted(data), color='#1f77b4', linewidth=2)

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(t)
    plt.show()

share_map = {}
inv_cnt = {}
inv_cntr=0

def get_shares(x):
    if(x in share_map):
        return len(share_map[x])
    else:
        return -1

# history_track=['0xbf200', '0x2a80', '0x1080', '0x1480', '0x4f40', '0x3280', '0x2a40', '0x1540', '0x1500', '0x14c0', '0x1ee2c0', '0xbf300', '0xbf2c0', '0xbf280', '0xbf240', '0x3300', '0x438ce00', '0x438cdc0', '0x59080', '0xbf440', '0xbf400', '0xbf3c0', '0xbf380', '0xbf340', '0x438d240', '0x43900c0', '0x438f2c0', '0x438d440', '0x438dcc0', '0x438d400', '0x438e180', '0x438e000', '0x438de00', '0x438db40', '0x438d980', '0x438d380', '0x438dbc0', '0x438d780', '0x438dd40', '0x438d300', '0x438da80', '0x438d600', '0x438dc40', '0x438d2c0', '0x438e140', '0x438dfc0', '0x438ddc0', '0x438d4c0', '0x438e040', '0x438d940', '0x438dc80', '0x438d500', '0x438d340', '0x438d9c0', '0x438d480', '0x438db00', '0x438d640', '0x438dd00', '0x438db80', '0x438d840', '0x438dac0', '0x438df80', '0x438da40', '0x438dd80', '0x438d5c0', '0x438e0c0', '0x438e080', '0x438d900', '0x438d3c0', '0x438d540', '0x438d800', '0x438de40', '0x438d7c0', '0x438d280', '0x438d580', '0x438da00', '0x438dc00', '0x438e100', '0x438e240', '0x438d740', '0x438df40', '0x438d680', '0x438df00', '0x438dec0', '0x438de80', '0x438d700', '0x438d6c0', '0x438d200', '0x438d1c0', '0x1440', '0x41b00', '0x1000', '0x5e400', '0x41a80', '0x1580', '0x217500', '0x217640', '0x13c0', '0x1380', '0x1400']
# history_track = history_track[:20]

# history_track =[]
address_info = {}
sys.argv.pop(0)
lc=0
total_lc = open(file_path,'r').read().count('\n')
one_per_cent_lc = int(total_lc/100)
progress=0
with open(file_path, 'r') as rf:
    while(1):
        lc+=1
        if((lc%one_per_cent_lc)==0):
            # if(progress>3):
            #     break
            print(progress, "% completed")
            progress+=1
        line = rf.readline()
        if(line.strip()==''):
            break
        if('NetDest' in line):
            bitmap = [int(kk) for kk in line.split('NetDest (20)  -')[1].split('-')[0].strip().split()]
            inv_processors =[]
            for i in range(len(bitmap)):
                if(bitmap[i] == 1):
                    inv_processors.append(i)
        elif('requester' in line):
            req = int(line.split('-')[-1])
        elif("Invalidation address" in line):
            address = line.split()[-1]
            a= address
            if(address in address_info):
                address_info[address].append({'req': req, 'inv': inv_processors})
            else:
                address_info[address] = [{'req': req, 'inv': inv_processors}]
            if(a in inv_cnt):
                inv_cnt[a] += len(inv_processors)
            else:
                inv_cnt[a] = len(inv_processors)
            inv_cntr += len(inv_processors)
        continue

#sorted_a = sorted(list(share_map), key=lambda x:len(share_map[x]))
#sizes = [len(share_map[a]) for a in sorted_a]
sorted_i = sorted(list(inv_cnt), key=lambda x:(inv_cnt[x]))
invs = [inv_cnt[a] for a in sorted_i]
cnts = sorted([inv_cnt[kk] for kk in inv_cnt])[::-1][:1000]
print(sorted_i[::-1][:100])
print(len(sorted_i))
print(sum(cnts)/inv_cntr)
# plt.plot(range(len((cnts))), sorted(cnts))
# plt.show()
print("Total Invs = ",inv_cntr)
print('DONE')
# exit()
##########


def plot_arrays(x, y1, y2, y3):
    # plt.figure(figsize=(8, 6))

    # Plot y1
    plt.plot(x, y1, label='Hierarchy',color='red')

    # Plot y2
    plt.plot(x, y2,label='Pointers',color='orange')

    # Plot y3
    plt.plot(x, y3, label='Group',color ='blue')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of y1, y2, and y3; against x')
    plt.legend()
    plt.grid(True)
    plt.show()


def log(x):
    return math.log(x)



def find_h_rep(p,limit,shared_processors):
    h_max = math.ceil(log(p / limit) / log(2))
    all_nodes = []
    for each_processor in shared_processors:
        h = ['h' + str(kk) + '_' + str(int(each_processor / pow(2, (kk + (int(log(limit*2) / log(2))))))) for kk in range(h_max)]
        all_nodes = list(set(all_nodes + h))  # this array is basically the total nodes in the entire tree we have touched so far
    return (len(all_nodes) * 2)


def de_res(n,shared_processors):
    c_inv_grps = set([int(kk / n) for kk in shared_processors])
    c_invs = []
    for i in c_inv_grps:
        c_invs += [n * i + (kk) for kk in range(n)]
    return c_invs


actual_extras = []
old_extras = []
perc_old_extras =[]
perc_actual_extras = []
saved_inv = []
perc_saved_inv = []
mode_2_sharers =[]
mode_4_sharers =[]
mode_8_sharers =[]
mode_history =[]
share_hist =[]
for a in address_info:
    ours = []
    dirs = []
    lims = []

    for each_inv in address_info[a]:
        if(bool(set(each_inv['inv'])-set([each_inv['req']]))):
            shared_processors = list(sorted([each_inv['req']]+each_inv['inv']))
            shared_processors = sorted(list(set([each_inv['req']]+each_inv['inv'])))
            ours_4 = find_h_rep(p,4,shared_processors)
            ours_2 = find_h_rep(p,2,shared_processors)
            count = len(shared_processors)
            dir_ = (log(p)/log(2))*count
            const_ = p/(limit)
            if(dir_ <=const_):
                mode= 'd'
            elif(ours_2<=const_):
                mode='2'
            else:
                mode='4'
            if(mode=='2'):
                my_invs= de_res(2,shared_processors)
                c_invs= de_res(4,shared_processors)
                if(each_inv['req'] in my_invs):
                    my_invs.remove(each_inv['req'])
                if (each_inv['req'] in c_invs):
                    c_invs.remove(each_inv['req'])
                actual_extras.append(len(set(my_invs)-set(shared_processors)))
                perc_actual_extras.append(100*len(set(my_invs)-set(shared_processors))/(len(shared_processors)))
                old_extras.append(len(set(c_invs) - set(shared_processors)))
                perc_old_extras.append(100 * len(set(c_invs) - set(shared_processors)) / (len(shared_processors)))

                mode_2_sharers.append(len(shared_processors))
                saved_inv.append((len(set(c_invs)-set(my_invs))))
                perc_saved_inv.append(100*(len(set(c_invs)-set(my_invs)))/len(my_invs))
            elif(mode=='4'):
                mode_4_sharers.append(len(shared_processors))
                my_invs = de_res(4, shared_processors)
                if (each_inv['req'] in my_invs):
                    my_invs.remove(each_inv['req'])
                actual_extras.append(len(set(my_invs) - set(shared_processors)))
                perc_actual_extras.append(100 * len(set(my_invs) - set(shared_processors)) / (len(shared_processors)))
                old_extras.append(len(set(my_invs) - set(shared_processors)))
                perc_old_extras.append(100 * len(set(my_invs) - set(shared_processors)) / (len(shared_processors)))
                saved_inv.append(0)
                perc_saved_inv.append(0)
            else:
                actual_extras.append(0)
                perc_actual_extras.append(0)
                saved_inv.append(0)
                perc_saved_inv.append(0)
                old_extras.append(0)
                perc_old_extras.append(0)
            mode_history.append(mode)
            share_hist.append(len(shared_processors))

            # if((mode==req_mode) and (len(shared_processors)>15)):
            #     print("count =", shared_processors,"ours_8 =", ours_8, "ours_4 =", ours_4, "ours_2 =", ours_2, "dir_ =", dir_, "const_ =", const_)
#     plot_arrays(shared,ours,dirs,lims)
def mean(x):
    if(len(x)==0):
        return -1
    return sum(x)/len(x)

def nz_mean(x):
    while(0 in x):
        x.remove(0)
    return mean(x)

print('act extra',mean(actual_extras))
print('% act extra',mean(perc_actual_extras))
print('old extra',mean(old_extras))
print('% old extra',mean(perc_old_extras))
print('saved inv',mean(saved_inv))
print('% saved inv',mean(perc_saved_inv))


print('2 mode%', mode_history.count('2')*100/len(mode_history))
print('4 mode%', mode_history.count('4')*100/len(mode_history))
print('d mode%', mode_history.count('d')*100/len(mode_history))

open(tag+'_plot.txt','w').write(str(mode_2_sharers)+'\n')
open(tag+'_plot.txt','a').write(str(mode_4_sharers)+'\n')
open(tag+'_plot.txt','a').write(str(mode_8_sharers)+'\n')
open(tag+'_plot.txt','a').write(str(share_hist)+'\n')
open(tag+'_plot.txt','a').write(str(mean(actual_extras))+'\n')
open(tag+'_plot.txt','a').write(str(mean(perc_actual_extras))+'\n')
open(tag+'_plot.txt','a').write(str(mean(old_extras))+'\n')
open(tag+'_plot.txt','a').write(str(mean(perc_old_extras))+'\n')
open(tag+'_plot.txt','a').write(str(mean(perc_saved_inv))+'\n')
open(tag+'_plot.txt','a').write(str(mode_history.count('2')*100/len(mode_history))+'\n')
open(tag+'_plot.txt','a').write(str(mode_history.count('4')*100/len(mode_history))+'\n')
open(tag+'_plot.txt','a').write(str(mode_history.count('d')*100/len(mode_history))+'\n')
open(tag+'_plot.txt','a').write(str(-1)+'\n')
percentile_plot(mode_2_sharers,'% of invalidation actions at Mode=2','Number of sharers','Mode-2 Percentile of sharers')
percentile_plot(mode_4_sharers,'% of invalidation actions at Mode=4','Number of sharers','Mode-4 Percentile of sharers')
percentile_plot(share_hist,'% of invalidation action overall','Number of sharers','Percentile of sharers')

# print('nz saved',nz_mean(saved_inv))
# print('%nz saved',nz_mean(perc_saved_inv))

# Sharing Pattern of our workload
