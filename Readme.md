# FIXD Technical project
This project aims to put together a dataset which involves combining two datasets and investigating the relation between number of cylinders and issues reported for vehicles
## Components of the project

### 1. Understanding Singer
Understanding the various aspects of communication over streams in the form of schema and records. The data aspects of dealing with a JSON like structure. Implementing the Taps and Targets to get the data into the different format itself was a fantastic learning experience and even though it took me a while to get used to piping the data using Singer, I was overjoyed when I finally got the hang of it and was able to pipeline the data to the required csv format from the Styles API
### 2. Installing Singer
I set up the virtual environment
```
python -m venv C:/Users/yashb/styles_tap
```
 and installed singer-python library
```
pip install singer-python
```

### 3. Creating a Singer Tap
First I created the schema for my tap and where I included the columns of make_name, model_name, year, trim, cylinder and sq_vins
```
schema = {'properties': {
        'make_name': {'type': ['string','null']},
        'model_name': {'type': ['string','null']},
        'year': {'type': ['integer','null']},
        'trim': {'type': ['string','null']},
        'cylinder' : {'type':['integer','null']},
        'sq_vins': {'type': ['string','null']}}}
```
Then using the URL and Response, using the requests library in python, I pulled the 1004 pages with 50 records per page.
After seeing that there were multiple VINs for each row, I the de-normalized the list of Squish VINs by creating different rows for each Squish VIN
### 4. Installing target-csv

I then installed the target of target-csv which converted the stream from tap to a target csv file
```
pip install target-csv
```
### 5. piping the Singer tap stream to target-csv
I created a config file containing the delimiter and destination path for the output csv file
Inside the virtual enviroment, upon writing the below command, I got the Styles API data into a csv file 
```
python styles_tapp.py | target-csv --config schema_style.conf
```
### 6. Reading the Styles data from CSV to combine the two dataset
The next step was to combine the two datasets. For this, I first read the styles csv file line by line, and then performed preprocessing on the data
### 7. Performing preprocessing on Styles data
I performed preprocessing on the styles data that was read. There were some rows that had the "trim" column flattened into multiple columned values.
I combined those values into one "trim" column. After creating a structed dataframe in pandas, I then removed the rows which had no cylinder values and the rows with cyinder values as 0.

### 8. Performing preprocessing on Issue Report data
Here, I created another column from the obfuscated_vin column denoting the Squish Vin and then returned the dataframe to combine this data with the styles data
### 9. Combining Styles and Issue Report data
I have used the squish_vin column in both the dataset to combine the two datasets using inner join operation
```
combined_data=pd.merge(data1_filtered,data2,how='inner')
```

### 10. Visualizing the combined dataset to view relation between number of cylinders vs issues reported
First I plotted a scatterplot between number of cylinders and issue counts column.
![Alt text](Scatterplot.png?raw=true "Scatterplot between number of cylinders and issue counts")
This showed higher peaks of issue counts in 6 and 8 cylinder vehicles.
After this, I plotted a boxplot for each of the number of cylinders. Checked if there are outlier values and then only considered issue count values <20 which reduced only 5% of the data.
This gave a better idea of the true range of issues to engine count and where most of the issue count values lie for n-cylindered vehicles.


