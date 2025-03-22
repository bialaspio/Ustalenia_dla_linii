# -*- coding: utf8 -*-
#!/usr/bin/python2.7
#
# Small script to show PostgreSQL and Pyscopg together
#

import sys,os,glob,psycopg2,csv,time, datetime, errno, json, collections
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from datetime import datetime
from collections import OrderedDict
	
#---------------------------------------------------------------------------------------------
def exec_query ( str_query ):
	try:
		cur.execute(str_query) 
		print 'Wykonane zapytanie '+str_query
	except Exception, e:
		print '	Nie udalo sie wykonac zapytania:'+str_query
		err_log.write('Nie udalo sie wykonac zapytania (select):'+str_query+'\n')
		print e
	return cur
#---------------------------------------------------------------------------------------------
	
def exec_query_commit( str_query ):
	try:
		cur.execute(str_query) 
		conn_PG.commit()
		print 'Wykonane zapytanie '+str_query
	except Exception, e:
		print '	Nie udalo sie wykonac zapytania:'+str_query
		print e
		err_log.write('Nie udalo sie wykonac zapytania (commit):'+str_query+'\n')
		os.system('pause')
	return cur 	
#------------------------------------------------------------------------------------------
def get_dresy():
	dirs_name = glob.glob ('adresy')
	#Stworzenie tablicy na dane z katalogu ADRESY_OK 
	drop_query = 'DROP TABLE IF EXISTS ADRESY_OK_0024l'
	exec_query_commit(drop_query)
	create_query = 'create table ADRESY_OK_0024l ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
	
	#Stworzenie tablicy na dane z katalogu ADRESY_BIP
	drop_query = 'DROP TABLE IF EXISTS ADRESY_BIP_all'
	exec_query_commit(drop_query)
	#create_query = 'create table ADRESY_BIP_all ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	create_query = 'create table ADRESY_BIP_all ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
			
	for dir_name in dirs_name:
		files_xls_names = glob.glob(dir_name+'\\*.xls*')
		print files_xls_names
		for file_xls_name in files_xls_names:
			print file_xls_name
#			os.system('pause')
			table_name = os.path.basename(file_xls_name)
			#table_name = table_name.split('.')[0]
			data = get_data(file_xls_name)
			
			licznik = 1
			for wiersz in data['PRAWIDLOWE_ADRESY']:
				if licznik > 1 and len(wiersz) > 1: 
					try:
						G = str(wiersz[0].encode('utf8'))
					except:
						G=""
					
					try:
						DZ = str(wiersz[1].encode('utf8'))
					except:
						DZ = ''
					
					try: 
						WL = str(wiersz[4].encode('utf8'))
					except:
						WL =''
					
					try:
						RODZICE = str(wiersz[5].encode('utf8'))
					except:
						RODZICE = ''
					
					try:
						ADRES_CZ2_POP = str(wiersz[8].encode('utf8'))
					except:
						ADRES_CZ2_POP = ''
					
					try:
						ADRES_CZ1_POP = str(wiersz[9].encode('utf8'))
					except:
						ADRES_CZ1_POP = ''
					#zaladowania danych do bazy   
					
					insert_query = "insert into ADRESY_OK_0024l VALUES ('"+DZ+"','"+WL+"','"+RODZICE+"','"+ADRES_CZ2_POP+"','"+ADRES_CZ1_POP+"','"+table_name+"');"
					print insert_query
					exec_query_commit(insert_query)	
				licznik = licznik+1
		
			licznik = 1
			print file_xls_name
			for wiersz in data['BiP_NIEPRAWIDLOWE_ADRESY']:
				if licznik > 1 and len(wiersz) > 1: 
					try:
						G = str(wiersz[0].encode('utf8'))
					except:
						G=''
					
					try:
						DZ = str(wiersz[1].encode('utf8'))
					except: 
						DZ = ''
					
					try:
						WL = str(wiersz[4].encode('utf8'))
					except:
						WL = ''
					
					try:
						RODZICE = str(wiersz[5].encode('utf8'))
					except:
						RODZICE = ''
						
					#zaladowania danych do bazy   
					insert_query = "insert into ADRESY_BIP_all VALUES ('"+DZ+"','"+WL+"','"+RODZICE+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1	
	
#------------------------------------------------------------------------------------------
def get_dresy_stykowe():
	dirs_name = glob.glob ('adr_stykowe')
	#Stworzenie tablicy na dane z katalogu ADRESY_OK_STYK 
	drop_query = 'DROP TABLE IF EXISTS ADRESY_OK_STYK'
	exec_query_commit(drop_query)
	create_query = 'create table ADRESY_OK_STYK ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
	
	#Stworzenie tablicy na dane z katalogu ADRESY_BIP_STYK
	drop_query = 'DROP TABLE IF EXISTS ADRESY_BIP_STYK'
	exec_query_commit(drop_query)
	#create_query = 'create table ADRESY_BIP_STYK ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	create_query = 'create table ADRESY_BIP_STYK ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
			
	for dir_name in dirs_name:
		files_xls_names = glob.glob(dir_name+'\\*.xls*')
		print files_xls_names
		for file_xls_name in files_xls_names:
			print file_xls_name
#			os.system('pause')
			table_name = os.path.basename(file_xls_name)
			table_name = table_name.split('.')[0]
			data = get_data(file_xls_name)
			
			licznik = 1
			for wiersz in data['PRAWIDLOWE_ADRESY']:
				if licznik > 1 and len(wiersz) > 1: 
					try:
						G = str(wiersz[0].encode('utf8'))
					except:
						G=""
					
					try:
						DZ = str(wiersz[1].encode('utf8'))
					except:
						DZ = ''
					
					try: 
						WL = str(wiersz[4].encode('utf8'))
					except:
						WL =''
					
					try:
						RODZICE = str(wiersz[5].encode('utf8'))
					except:
						RODZICE = ''
					
					try:
						ADRES_CZ2_POP = str(wiersz[8].encode('utf8'))
					except:
						ADRES_CZ2_POP = ''
					
					try:
						ADRES_CZ1_POP = str(wiersz[9].encode('utf8'))
					except:
						ADRES_CZ1_POP = ''
					#zaladowania danych do bazy   
					insert_query = "insert into ADRESY_OK_STYK VALUES ('"+DZ+"','"+WL+"','"+RODZICE+"','"+ADRES_CZ2_POP+"','"+ADRES_CZ1_POP+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1
		
			licznik = 1
			print file_xls_name
			for wiersz in data['BiP_NIEPRAWIDLOWE_ADRESY']:
				if licznik > 1 and len(wiersz) > 1: 
					try:
						G = str(wiersz[0].encode('utf8'))
					except:
						G=''
					
					try:
						DZ = str(wiersz[1].encode('utf8'))
					except: 
						DZ = ''
					
					try:
						WL = str(wiersz[4].encode('utf8'))
					except:
						WL = ''
					
					try:
						RODZICE = str(wiersz[5].encode('utf8'))
					except:
						RODZICE = ''
						
					#zaladowania danych do bazy   
					insert_query = "insert into ADRESY_BIP_STYK VALUES ('"+DZ+"','"+WL+"','"+RODZICE+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1	
	#zrobienie kolumny odpowiadajacej adresa dla adresow stykowych zapisanych jako zlozenie nr_teryt i dzialki 
	alter_query = "alter table ADRESY_OK_STYK add kerg_dz character varying(150);"
	exec_query_commit(alter_query)
	update_query = "update ADRESY_OK_STYK kerg_dz set kerg_dz = replace (substring(plik_csv,0,14), '_0', '.0')||'.'||dz;"
	exec_query_commit(update_query)
	alter_query = "alter table ADRESY_BIP_STYK add kerg_dz character varying(150);"
	exec_query_commit(alter_query)
	update_query = "update ADRESY_BIP_STYK kerg_dz set kerg_dz = replace (substring(plik_csv,0,14), '_0', '.0')||'.'||dz;"
	exec_query_commit(update_query)

#----------------------------------------------------------------------------------------------------------------------------------		

def get_data_from_ZAWIADOMIENIA():
	dirs_name = glob.glob ('zawiadomienia')
	#Stworzenie tablicy na dane z katalogu ZAWIADOMIENIA 
	drop_query = 'DROP TABLE IF EXISTS ZAWIADOMIENIA'
	exec_query_commit(drop_query)
	
	create_query = 'create table ZAWIADOMIENIA ( DATA character varying(1500), GODZINA character varying(1500), G character varying(500),	DDD character varying(1500),	KW character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2 character varying(1500), ADRES_CZ1 character varying(1500),	pwpt character varying(4500), plik_csv character varying(1500))'

	exec_query_commit(create_query)
			
	for dir_name in dirs_name:
		files_xls_names = glob.glob(dir_name+'\\*.xls*')
		print files_xls_names
		for file_xls_name in files_xls_names:
			print file_xls_name
			table_name = os.path.basename(file_xls_name)
			table_name = table_name.split('.')[0]
			data = get_data(file_xls_name)
			licznik = 1
			LP =''
			for wiersz in data['Arkusz1']:
				if licznik > 1 and len(wiersz) > 1: 
					
					DATA = str(wiersz[2].encode('utf8'))
					GODZINA = str(wiersz[3].encode('utf8'))
					G = str(wiersz[4].encode('utf8'))
					DDD = str(wiersz[5].encode('utf8'))
					KW = str(wiersz[6].encode('utf8'))
					WL = str(wiersz[9].encode('utf8'))
					RODZICE = str(wiersz[10].encode('utf8'))
					ADRES_CZ2 = str(wiersz[12].encode('utf8'))
					ADRES_CZ1 = str(wiersz[11].encode('utf8'))
					pwpt = str(wiersz[17].encode('utf8'))
					#zaladowania danych do bazy   
					insert_query = "insert into ZAWIADOMIENIA VALUES ('"+DATA+"','"+GODZINA+"','"+G+"','"+DDD+"','"+KW+"','"+WL+"','"+RODZICE+"','"+ADRES_CZ2+"','"+ADRES_CZ1+"','"+pwpt+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1

#----------------------------------------------------------------------------------------------------------------------------------		

def update_adresy():
	alter_query= "alter table ZAWIADOMIENIA drop if exists adr_cz2_pop;"
	exec_query_commit(alter_query)	
	alter_query = "alter table ZAWIADOMIENIA drop if exists adr_cz1_pop;"
	exec_query_commit(alter_query)		

	
	alter_query= "alter table ZAWIADOMIENIA add adr_cz2_pop character varying(1500);"
	exec_query_commit(alter_query)	
	alter_query = "alter table ZAWIADOMIENIA add adr_cz1_pop character varying(1500);"
	exec_query_commit(alter_query)	
	
	update_query = "update ZAWIADOMIENIA A set adr_cz2_pop = (select string_agg(DISTINCT ADRES_CZ2_POP,'---')  from ADRESY_OK B where (B.dz like A.ddd OR A.ddd like '%,'||B.dz||',%' OR A.ddd like B.dz||',%' OR A.ddd like '%,'||B.dz OR A.ddd like '%'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE) ;"
	exec_query_commit(update_query)
	
	#update_query = "update ZAWIADOMIENIA A set adr_cz1_pop = (select string_agg(DISTINCT ADRES_CZ1_POP,'--') from ADRESY_OK B where (B.dz like A.ddd OR A.ddd like '%,'||B.dz||',%' OR A.ddd like B.dz||',%' OR A.ddd like '%,'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE);"
	update_query = "update ZAWIADOMIENIA A set adr_cz1_pop = (select string_agg(DISTINCT ADRES_CZ1_POP,'---')  from ADRESY_OK B where (B.dz like A.ddd OR A.ddd like '%,'||B.dz||',%' OR A.ddd like B.dz||',%' OR A.ddd like '%,'||B.dz OR A.ddd like '%'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE);"
	exec_query_commit(update_query)
	
	
	update_query = "update ZAWIADOMIENIA A set adr_cz2_pop = 	(select DISTINCT 'BIP' from ADRESY_BIP B where (B.dz like A.ddd OR A.ddd like '%,'||B.dz||',%' OR A.ddd like B.dz||',%' OR A.ddd like '%,'||B.dz OR A.ddd like '%'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE) where ddd in (select ddd from ZAWIADOMIENIA AA, ADRESY_BIP BB where (BB.dz like AA.ddd OR AA.ddd like '%,'||BB.dz||',%' OR AA.ddd like BB.dz||',%' OR AA.ddd like '%,'||BB.dz  OR AA.ddd like '%'||BB.dz ) AND AA.WL=BB.WL AND AA.RODZICE=BB.RODZICE) and adr_cz2_pop is null;"
	exec_query_commit(update_query)
	
	update_query = "update ZAWIADOMIENIA A set adr_cz2_pop =	(select string_agg(DISTINCT ADRES_CZ2_POP,'---') from ADRESY_OK_STYK B where (B.kerg_dz like A.ddd OR A.ddd like '%,'||B.kerg_dz||',%' OR A.ddd like B.kerg_dz||',%' OR A.ddd like '%,'||B.kerg_dz  OR A.ddd like '%'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE) where ddd in (select ddd from ZAWIADOMIENIA AA, ADRESY_OK_STYK BB where (BB.kerg_dz like AA.ddd OR AA.ddd like '%,'||BB.kerg_dz||',%' OR AA.ddd like BB.kerg_dz||',%' OR AA.ddd like '%,'||BB.kerg_dz OR AA.ddd like '%'||BB.dz) AND AA.WL=BB.WL AND AA.RODZICE=BB.RODZICE) and adr_cz2_pop is null ;"
	exec_query_commit(update_query)
	
	update_query = "update ZAWIADOMIENIA A set adr_cz1_pop = (select string_agg(DISTINCT ADRES_CZ1_POP,'---') from ADRESY_OK_STYK B where (B.kerg_dz like A.ddd OR A.ddd like '%,'||B.kerg_dz||',%' OR A.ddd like B.kerg_dz||',%' OR A.ddd like '%,'||B.kerg_dz OR A.ddd like '%'||B.dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE) where ddd in (select ddd from ZAWIADOMIENIA AA, ADRESY_OK_STYK BB where (BB.kerg_dz like AA.ddd OR AA.ddd like '%,'||BB.kerg_dz||',%' OR AA.ddd like BB.kerg_dz||',%' OR AA.ddd like '%,'||BB.kerg_dz) AND AA.WL=BB.WL AND AA.RODZICE=BB.RODZICE OR AA.ddd like '%'||BB.dz)and adr_cz1_pop is null; "
	exec_query_commit(update_query)
	
	update_query = "update ZAWIADOMIENIA A set adr_cz2_pop = (select DISTINCT 'BIP' from ADRESY_BIP_STYK B where (B.kerg_dz like A.ddd OR A.ddd like '%,'||B.kerg_dz||',%' OR A.ddd like B.kerg_dz||',%' OR A.ddd like '%,'||B.kerg_dz) AND A.WL=B.WL AND A.RODZICE=B.RODZICE  OR A.ddd like '%'||B.dz) 	where ddd in (select ddd from ZAWIADOMIENIA AA, ADRESY_BIP_STYK BB where (BB.kerg_dz like AA.ddd OR AA.ddd like '%,'||BB.kerg_dz||',%' OR AA.ddd like BB.kerg_dz||',%' OR AA.ddd like '%,'||BB.kerg_dz) AND AA.WL=BB.WL AND AA.RODZICE=BB.RODZICE OR AA.ddd like '%'||BB.dz) and adr_cz2_pop is null; "
	exec_query_commit(update_query)

	
#--------------------------------------------------------------------------------------------------------------------------------------------	
def create_xlsx ():
	cur_local_select = conn_PG.cursor()
	data = OrderedDict()
	select_query = "select data, godzina, g, ddd, kw, wl, rodzice, adr_cz2_pop as adres_cz2, adres_cz1 as adr_cz1_pop, pwpt from ZAWIADOMIENIA"
	cur_local_select.execute(select_query) 
	lista = []
	for row_local_select in cur_local_select.fetchall():
		linia = row_local_select[0]+','+row_local_select[1]+','+row_local_select[2]+','+row_local_select[3]+','+row_local_select[4]+','+row_local_select[5]+','+row_local_select[6]+','+row_local_select[7]+','+row_local_select[8]+','+row_local_select[9]
		#print linia
		lista.append(linia)
	
	#data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
	#data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
	#save_data("your_file.xls", data)	

#--------------------------------------------------------------------------------------------------------------------------------------------
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#--------------------------------------------------------------------------------------------------------------------------------------------
if not os.path.exists('.\\log'):
    try:
        os.makedirs('.\\log')
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

naz_lik_log = time.strftime('%Y%m%d-%H_%M_%S')
naz_log = open('.\\log\\copy'+naz_lik_log+'.log', 'w')
err_log = open('.\\log\\ERR'+naz_lik_log+'.log', 'w')


#polacznie z baza POSTGRES 
teraz = time.asctime( time.localtime(time.time()))
try:
	conn_PG = psycopg2.connect("dbname='__dbname__' user='__user__' host='__host__' password='__passwd__' port='5432'")
	naz_log.write(teraz + ' [INF] Polaczono z baza danych\n')
except:
	print 'I am unable to connect to the database'
	err_log.write(teraz +' - [ERR] Nie udalo sie naiazac polacznia z baz\n')

cur = conn_PG.cursor()
#get_data_from_ZAWIADOMIENIA()
get_dresy()
#get_dresy_stykowe()
#update_adresy()
#create_xlsx () 