# Imports
import pandas as pd
from csv import reader
import matplotlib.pyplot as plt

# Functions
# Reading the Styles Singer Targetted data
def read_styles_data():
    dictionary = {}
    #reading data from the singer targetted csv file
    with open('styles-20210526T133336.csv','r') as fr:
        csv_reader=reader(fr)
        header=next(csv_reader)
        uniq_lens=[]
        col_list=['make_name', 'model_name', 'year', 'trim','cylinder', 'sq_vins']

        for col in col_list:
            dictionary[col]=[]


        for row in csv_reader:
            # Checking for rows that have flattened trim values showing more values in a row than the number of columns
            if len(row)>6:
                if len(row) not in uniq_lens:
                    uniq_lens.append(len(row))
                # Checking for 7 values in a row
                if len(row)==7:
                    row_ind=0
                    col_ind=0
                    while(col_ind<len(col_list)):
                        # Combining the trim columns into a single value
                        if col_list[col_ind]=="trim":
                            trimval=row[row_ind]+row[row_ind+1]
                            dictionary[col_list[col_ind]].append(trimval)
                            row_ind+=1
                        else:
                            dictionary[col_list[col_ind]].append(row[row_ind])
                        row_ind+=1
                        col_ind+=1
                # Checking for 7 values in a row
                elif len(row)==8:
                    row_ind = 0
                    col_ind = 0
                    while (col_ind < len(col_list)):
                        # Combining the trim columns into a single value
                        if col_list[col_ind] == "trim":
                            trimval = row[row_ind] + row[row_ind + 1] + row[row_ind + 2]
                            dictionary[col_list[col_ind]].append(trimval)
                            row_ind += 2
                        else:
                            dictionary[col_list[col_ind]].append(row[row_ind])
                        row_ind += 1
                        col_ind += 1

            elif len(row)==6:
                for col_ind in range(len(col_list)):
                    dictionary[col_list[col_ind]].append(row[col_ind])
            else:
                continue
        print(header)
        print(uniq_lens)
    #Creating a dataframe out of the dictionary and returning the data
    data1=pd.DataFrame(dictionary,columns=header)
    return data1
    pass
def read_issue_report():
    df=pd.read_csv("issue_counts.csv")
    print(df.head())
    # Created Squish VINs from Obfuscated VINs
    df['sq_vins']=df['obfuscated_vin'].str[:8]+df['obfuscated_vin'].str[9:11]
    print(df.head())
    return df
def combine_datasets():
    # Read Issue Report Data
    data2=read_issue_report()
    # Reading Styles Data
    data1=read_styles_data()
    print(data1.head())
    print(len(data1))
    # Checked unique number of cylinder
    print(data1['cylinder'].unique())
    print(len(data1))
    # Removed empty values for cylinders
    data1_filtered = data1[data1['cylinder'] != '']
    # Converted the data type of cylinders from string to integers
    data1_filtered=data1_filtered.astype({'cylinder':'int'})
    # filtered rows for vehicles that have 0 cylinders
    data1_filtered=data1_filtered[data1_filtered['cylinder']>0]
    print(len(data1_filtered))
    # merged the two dataset by performing inner join on the Squish VINs of both datasets
    combined_data=pd.merge(data1_filtered,data2,how='inner')
    print(combined_data.head())
    print(len(combined_data))
    # Removed about 5% of the data with very high issue count treating them as outliers
    combined_data=combined_data[combined_data['issue_count']<20]
    print(len(combined_data))
    grouped_data=combined_data.groupby(['cylinder'])#.agg({'issue_count'})

    # Created boxplots for each of the grouped data for each number of cylinders
    for key,item in grouped_data:
        a_group=grouped_data.get_group(key)

        #a_group_count=a_group.groupby(['issue_count']).count()
        #print(a_group_count)
        #plt.bar(a_group['issue_count'].unique(),a_group_count['id'])
        #plt.show()
        plt.boxplot(a_group['issue_count'],labels=[key])
        plt.title("Boxplot for issue counts of "+str(key)+" number of cylinders")
        plt.show()


#Main Program
combine_datasets()