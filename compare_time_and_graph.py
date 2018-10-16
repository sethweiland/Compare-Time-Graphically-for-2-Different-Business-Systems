import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyodbc

# lists of tuples that we will loop through with matching business lines used in 2 different systems
queue_tuples= [ ('1018', 'Credit Review (CDL)'),('1017', 'Closing Review'),	('1020', 'DTI Review'),	('1016', 'Funding Review'), ('1008', 'Loan Structure Review (CDL)'), ('1021', 'Title Review')]
encompass_tuples = [('1008', 'Loan Structure Review (CDL)'),('1016', 'Funding Review'),	('1017', 'Closing Review'),	('1018', 'Credit Review (CDL)'),('1020', 'DTI Review'),	('1021', 'Title Review')]



queue_dict= dict(queue_tuples)

#headers for one the pandas dataframes we will create
encompass_headers=['process_name', 'month_start','avg_time_in_month(hours)', 'count_in_month']

#two seperate pandas df, one for each business line studied
df_allocation = pd.read_csv('count_average_per_month.csv')
df_encompass = pd.read_csv('count_average_encompass.csv', header=None, names=encompass_headers)

unique_encompass = df_encompass['process_name'].unique()
unique_queue = df_allocation['queue_id'].unique()
print(len(unique_queue))
for value, name in zip(queue_tuples, unique_encompass):
    if value[0] not in ('1008', '1016', '1017', '1018', '1020', '1021'):
        continue
    #splice these dataframes within our loop to isolate all rows that represent a time transaction for a given business line
    df_specific_all = df_allocation[df_allocation['queue_id'] == int(value[0])]
    df_more_specific_all = df_specific_all[df_specific_all['created_month']<12]
    df_specific_encompass = df_encompass[df_encompass['process_name']==name]
    df_more_specific_encompass = df_specific_encompass[df_specific_encompass['month_start']<12]
    #create plt figure and create 2 graphs that will sit in same figure, with each figure representing monthly averages times per transaction
    #for given business periods
    fig=plt.figure(figsize = (10, 10))
    ax_all=fig.add_subplot(1,2,1)
    ax_enc = fig.add_subplot(1, 2, 2)
    ax_all.bar(df_more_specific_all['created_month'], df_more_specific_all['avg_time_in_queue'], color='black', label=str(value[0]))
    ax_enc.bar(df_more_specific_encompass['month_start'], df_more_specific_encompass['avg_time_in_month(hours)'])
    ax_all.tick_params(top=False, bottom=False, left=False, right=False)
    ax_enc.tick_params(top=False, bottom=False, left=False, right=False)
    ax_all.set_xlim(0, 12)
    ax_enc.set_xlim(0, 12)
    ax_all.set_ylim(0, df_more_specific_encompass['avg_time_in_month(hours)'].max()+5)
    ax_enc.set_ylim(0, df_more_specific_encompass['avg_time_in_month(hours)'].max() + 5)
    ax_all.set_xlabel('Month')
    ax_enc.set_xlabel('Month')
    ax_all.set_ylabel('Time (hours)')
    ax_enc.set_ylabel('Time (hours)')
    ax_all.set_title('Time in queue for ' + str(queue_dict[str(value[0])])+' ('+str(value[0])+')')
    ax_enc.set_title('Time in encompass for ' + name + '(CDL)')
    spines=ax_all.spines
    spines1 = ax_enc.spines
    ax_all.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax_enc.xaxis.set_major_locator(plt.MaxNLocator(12))
    bars=ax_all.patches
    bars1 = ax_enc.patches
    #create histograms labels based on how many of each transaction happened in a given month to suplement the time-based analysis. 
    labels=[value for value in df_specific_all['count_fr_month']]
    for bar, label in zip(bars, labels):
        height=bar.get_height()
        ax_all.text(bar.get_x() + bar.get_width() /2, height+1,label, ha='center', va='bottom')
    file_id=str(queue_dict[str(value[0])])
    #file name edited out
    file_name=('file name not given due to security concern' + file_id +'_('+str(value[0])+')'+'.png')
    #save each pair of graphs to a png file within our loop for each business line. 
    plt.savefig(file_name, bbox_inches="tight")
    plt.show()
