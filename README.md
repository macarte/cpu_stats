# cpu_stats
python files for efficiently capturing multi-core cpu usage

we use the psutil module (documentation: https://psutil.readthedocs.io/en/latest/)

step 1) install dependencies (psutil)

````
pip install -r requirements.txt
````

step 2) record cpu stats, sampling cores every 10ms

````
python3 cpu_stat.py --sample 0.01 --binary_output mystats.bin
````

step 3) convert the binary file to a csv (with header)

````
python3 cpu_stat_to_csv.py --binary_input mystats.bin --header >mystats.csv
````

step 4) open the jupyter notebook and make sure to load the csv file by changing the following line

````
dataframe = pandas.read_csv("mystats.csv")
````
# TODO

1) determine cost of cpu_stat.py
2) record user/kernel(sys) splits
3) monitor pid
4) spawn process and monitor pid