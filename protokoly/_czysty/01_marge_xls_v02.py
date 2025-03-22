import sys,os,glob,psycopg2,shutil,distutils.core,time, datetime, string, csv
from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd

main_dir = os.getcwd()
main_dir_name = main_dir+'\\protokoly\\'

dirs_name = glob.glob ('protokoly\\*.xls')
prot_list = []

for dir_name in dirs_name:
	file_name = dir_name.split('\\',2) 
	prot_list.append(file_name[1][:3])
prot_list = list(set(prot_list)) 

for prot in prot_list:
	print 'Lazcze pliki :'+ str(prot)
	path= main_dir_name+prot+'*'
	excel_names = glob.glob(path)
	# read them in
	excels = [pd.ExcelFile(name) for name in excel_names]
	# turn them into dataframes
	if excels:
		frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
		#print frames
			# delete the first row for all frames except the first
			# i.e. remove the header row -- assumes it's the first
		frames[1:] = [df[7:] for df in frames[1:]]
		# concatenate them..
		combined = pd.concat(frames)	
		# write it out
		combined.to_excel("out\\bez_format\\"+prot+".xlsx", header=False, index=False)
os.system("pause")