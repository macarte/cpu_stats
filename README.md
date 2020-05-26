# cpu_stats
python files for efficiently capturing multi-core cpu usage

step 1) record cpu stats, sampling cores every 10ms

````
python3 cpu_stat.py --sample 0.01 --binary_output mystats.bin
````

step 2) convert the binary file to a csv (with header)

````
python3 cpu_stat_to_csv.py --binary_input mystats.bin --header >mystats.csv
````

step 3) open the jupyter notebook and make sure to load the csv file by changing the following line

````
dataframe = pandas.read_csv("mystats.csv")
````
