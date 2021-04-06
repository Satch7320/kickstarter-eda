import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


late_csv = pd.read_csv('ks-projects-201801.csv')

def make_hist(x):
    fig, ax = plt.subplots()
    return ax.hist(x)

def subtable(category):
    df = late_csv[late_csv['main_category'] == category]
    return df

def bootstrap(samp, num_bs_sam = 10000):
    bs = []
    
    for _ in range(num_bs_sam):
        bs.append(np.random.choice(samp, size = len(samp)))
        
    return bs

def bootstrap_ci(sample, stat_function=np.mean, num_resamp = 10000, ci = .95):
    bs = bootstrap(sample, num_resamp)
    
    stat_list = []
    
    for row in range(len(bs)):
        stat_list.append(np.percentile(stat_function(bs[row]),ci))
        #print(row)
    
    return np.percentile(sample,ci), stat_list

def series_norm(series):
    return (series - series.mean()) / (series.max() - series.min())

cats = set(late_csv['main_category'])
sub_cats = set(late_csv['category'])
state_number_map = {'failed':0, 'successful':1, 'live':2, 
                    'suspended':3, 'canceled':4, 'undefined':5}
                    
late_csv['launched'] = pd.to_datetime(late_csv['launched'])
late_csv['deadline'] = pd.to_datetime(late_csv['deadline'])
late_csv['state'] = late_csv['state'].map(state_number_map)
late_csv['length'] = late_csv['deadline'] - late_csv['launched']

av_pledge = late_csv.groupby('main_category')
backers_counts = av_pledge['backers'].count()

f_and_v = subtable('Film & Video')
