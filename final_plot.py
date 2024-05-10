import matplotlib.pyplot as plt
import seaborn as sns
styles=[True,True,[2,2],True,[2,2]]
styles=[True,True,[2,2],True,[2,2]]
colors = ['red','blue','yellow','black']
def perc_plot1(arrays):
    sns.set_style("darkgrid")
    cntr=0
    for each in arrays:
        data= each[0]
        label= each[1]
        x_ = [kk * 100 / (len(data)) for kk in (range(len(data)))]
        data = sorted(data)
        # plt.plot(x_, data, label=each[1])
        sns.lineplot(x=x_, y=sorted(sorted(data)), linewidth=2,label=label,dashes=styles[cntr],colors=colors[cntr])
        cntr+=1
    plt.show()

def perc_plot(arrays):
    sns.set_style("darkgrid")
    cntr=0
    # arrays = [arrays[0],arrays[2]]
    # arrays = [arrays[0],arrays[2],arrays[4]]
    arrays = [arrays[0+1],arrays[2+1],arrays[4+1]]
    for each in arrays[:]:
        data= each[0]
        label= each[1]
        x_ = range(max(data))
        y_ = [data.count(kk+1) for kk in x_]
        y_ =[kk*100/len(data) for kk in y_]

        sns.lineplot(x=x_, y=y_, linewidth=2,label=label,dashes=styles[cntr])
        cntr+=1
    plt.xlabel('\'N\' Number of Processors')
    plt.ylabel('% of cachelines sharing \'N\' proces')
    plt.show()
total_lu_128 = [int(kk) for kk in open('tag_lu_128_plot.txt','r').read().split('\n')[3][1:-1].split(',')]
total_lu_64 = [int(kk) for kk in open('tag_lu_64_plot.txt','r').read().split('\n')[3][1:-1].split(',')]

total_ep_128 = [int(kk) for kk in open('tag_ep_128_plot.txt','r').read().split('\n')[3][1:-1].split(',')]
total_ep_64 = [int(kk) for kk in open('tag_ep_64_plot.txt','r').read().split('\n')[3][1:-1].split(',')]
#
total_cg_128 = [int(kk) for kk in open('tag_cg_128_plot.txt','r').read().split('\n')[3][1:-1].split(',')]
total_cg_64 = [int(kk) for kk in open('tag_cg_64_plot.txt','r').read().split('\n')[3][1:-1].split(',')]

# perc_plot([[total_cg_128,'cg_128'],[total_cg_64,'cg_64'],[total_lu_128,'lu_128'],[total_lu_64,'lu_64'],[total_ep_128,'ep_128'],[total_ep_64,'ep_64']])
# perc_plot([[total_cg_128,'cg_128']])
# exit()
# exit()


def get_128_dist(file_name):
    data = open(file_name, 'r').read().strip().split('\n')
    data = [(kk.count(',')+1) for kk in data[:]]
    data=  [data[0], data[1], data[2], data[3]-sum(data[:3])]
    data = [(kk*100/sum(data)) for kk in data]
    return data
def get_64_dist(file_name):
    data = open(file_name, 'r').read().strip().split('\n')
    data = [(kk.count(',')+1) for kk in data[:]]
    data = [data[0], data[1], data[3]-sum(data[:2])]
    data = [(kk * 100 / sum(data)) for kk in data]
    return data


def get_stats(file_name):
    data = open(file_name,'r').read().strip().split('\n')
    data =[float(kk) for kk in  data[4:]]
    return data

def hist_plot(data,labels,title):
    colors = ['blue', 'green', 'orange', 'red','black','violet','yellow']

    # Plotting
    sns.barplot(x=labels, y=data, palette=colors)
    # Adding labels for each bar
    for i, v in enumerate(data):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
    # Adding labels and title
    plt.xlabel('Mode')
    plt.ylabel('%')
    plt.title(title)
    # Display plot
    plt.show()

lu_128_dist = get_128_dist('tag_lu_128_plot.txt')
lu_64_dist = get_64_dist('tag_lu_64_plot.txt')
ep_128_dist = get_128_dist('tag_ep_128_plot.txt')
ep_64_dist = get_64_dist('tag_ep_64_plot.txt')
cg_128_dist = get_128_dist('tag_cg_128_plot.txt')
cg_64_dist = get_64_dist('tag_cg_64_plot.txt')

lu_128_stats = get_stats('tag_lu_128_plot.txt')
lu_64_stats = get_stats('tag_lu_64_plot.txt')
ep_128_stats = get_stats('tag_ep_128_plot.txt')
ep_64_stats = get_stats('tag_ep_64_plot.txt')
cg_128_stats = get_stats('tag_cg_128_plot.txt')
cg_64_stats = get_stats('tag_cg_64_plot.txt')


# hist_plot([kk[3] for kk in [lu_128_stats,lu_64_stats,ep_128_stats,ep_64_stats,cg_128_stats, cg_64_stats]],['lu_128','lu_64','ep_128','ep_64','cg_128','cg_64'],'% Extra Invalidations For DIRiCVr')
# hist_plot([kk[1] for kk in [lu_128_stats,lu_64_stats,ep_128_stats,ep_64_stats,cg_128_stats, cg_64_stats]],['lu_128','lu_64','ep_128','ep_64','cg_128','cg_64'],'% Extra Invalidations For HCV')
hist_plot([kk[4] for kk in [lu_128_stats,lu_64_stats,ep_128_stats,ep_64_stats,cg_128_stats, cg_64_stats]],['lu_128','lu_64','ep_128','ep_64','cg_128','cg_64'],'% Savings in Inv Traffic')
hist_plot(lu_128_dist, ['mode_2','mode_4','mode_8','mode_dir(i)'],'lu_128 mode distribution %')
hist_plot(lu_64_dist, ['mode_2','mode_4','mode_dir(i)'],'lu_64 mode distribution %')
hist_plot(ep_128_dist, ['mode_2','mode_4','mode_8','mode_dir(i)'],'ep_128 mode distribution %')
hist_plot(ep_64_dist, ['mode_2','mode_4','mode_dir(i)'],'ep_64 mode distribution %')
hist_plot(cg_128_dist, ['mode_2','mode_4','mode_8','mode_dir(i)'],'cg_128 mode distribution %')
hist_plot(cg_64_dist, ['mode_2','mode_4','mode_dir(i)'],'cg_64 mode distribution %')
