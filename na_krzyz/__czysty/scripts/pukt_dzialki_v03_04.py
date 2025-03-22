import sys,os,glob,psycopg2,shutil,distutils.core,time, datetime, string, csv
from pyexcel_xls import get_data
from pyexcel_xls import save_data

# Odczytanie pliku

#---------------------------------------------------------------------------------------------
def exec_query ( str_query ):
	try:
		cur.execute(str_query) 
		print ('Wykonane zapytanie '+str_query)
	except :
		print ('	Nie udalo sie wykonac zapytania:'+str_query)
		err_log.write('Nie udalo sie wykonac zapytania (select):'+str_query+'\n')
		os.system('pause')
	return cur


#---------------------------------------------------------------------------------------------
	
def exec_query_commit( str_query ):
	#try:
		cur.execute(str_query) 
		conn_PG.commit()
		print ('Wykonane zapytanie '+str_query)
	#except:
	#	print ('	Nie udalo sie wykonac zapytania:'+str_query)
	#	err_log.write('Nie udalo sie wykonac zapytania (commit):'+str_query+'\n')
	#	os.system('pause')
		return cur 	

#---------------------------------------------------------------------------------------------	
def get_dresy():
	dirs_name = glob.glob ('adresy')
	#Stworzenie tablicy na dane z katalogu ADRESY_G_OK 
	drop_query = 'DROP TABLE IF EXISTS ADRESY_G_OK'
	exec_query_commit(drop_query)
	create_query = 'create table ADRESY_G_OK (  G character varying(1500),DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
	#Stworzenie tablicy na dane z katalogu ADRESY_G_BIP
	drop_query = 'DROP TABLE IF EXISTS ADRESY_G_BIP'
	exec_query_commit(drop_query)
	#create_query = 'create table ADRESY_G_BIP ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	create_query = 'create table ADRESY_G_BIP ( G character varying(1500),DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
	print (dirs_name) 		
	for dir_name in dirs_name:
		
		files_xls_names = glob.glob(dir_name+'\\*.xls*')
		print (files_xls_names)
		for file_xls_name in files_xls_names:
			print (file_xls_name)
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
					insert_query = "insert into ADRESY_G_OK VALUES ('"+G+"','"+DZ+"','"+WL+"','"+RODZICE+"','"+ADRES_CZ2_POP+"','"+ADRES_CZ1_POP+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1
		
			licznik = 1
			print (file_xls_name)
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
					insert_query = "insert into ADRESY_G_BIP VALUES ('"+G+"','"+DZ+"','"+WL+"','"+RODZICE+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1
	

#------------------------------------------------------------------------------------------
def get_dresy_stykowe():
	dirs_name = glob.glob ('adr_stykowe')
	#Stworzenie tablicy na dane z katalogu ADRESY_G_OK_STYK 
	drop_query = 'DROP TABLE IF EXISTS ADRESY_G_OK_STYK'
	exec_query_commit(drop_query)
	create_query = 'create table ADRESY_G_OK_STYK ( G character varying(50),DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
	
	#Stworzenie tablicy na dane z katalogu ADRESY_G_BIP_STYK
	drop_query = 'DROP TABLE IF EXISTS ADRESY_G_BIP_STYK'
	exec_query_commit(drop_query)
	#create_query = 'create table ADRESY_G_BIP_STYK ( DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500),ADRES_CZ2_POP character varying(1500), ADRES_CZ1_POP character varying(1500), plik_csv character varying(1500))'
	create_query = 'create table ADRESY_G_BIP_STYK ( G character varying(50),DZ character varying(1500),	WL character varying(1500),	RODZICE character varying(1500), plik_csv character varying(1500))'
	exec_query_commit(create_query)
			
	for dir_name in dirs_name:
		files_xls_names = glob.glob(dir_name+'\\*.xls*')
		print (files_xls_names)
		for file_xls_name in files_xls_names:
			print (file_xls_name)
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
					insert_query = "insert into ADRESY_G_OK_STYK VALUES ('"+G+"','"+DZ+"','"+WL+"','"+RODZICE+"','"+ADRES_CZ2_POP+"','"+ADRES_CZ1_POP+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1
		
			licznik = 1
			print (file_xls_name)
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
					insert_query = "insert into ADRESY_G_BIP_STYK VALUES ('"+G+"','"+DZ+"','"+WL+"','"+RODZICE+"','"+table_name+"');"
					exec_query_commit(insert_query)	
				licznik = licznik+1	
	#zrobienie kolumny odpowiadajacej adresa dla adresow stykowych zapisanych jako zlozenie nr_teryt i dzialki 
	alter_query = "alter table ADRESY_G_OK_STYK add kerg_dz character varying(150);"
	exec_query_commit(alter_query)
	update_query = "update ADRESY_G_OK_STYK kerg_dz set kerg_dz = replace (substring(plik_csv,0,14), '_0', '.0')||'.'||dz;"
	exec_query_commit(update_query)
	alter_query = "alter table ADRESY_G_BIP_STYK add kerg_dz character varying(150);"
	exec_query_commit(alter_query)
	update_query = "update ADRESY_G_BIP_STYK kerg_dz set kerg_dz = replace (substring(plik_csv,0,14), '_0', '.0')||'.'||dz;"
	exec_query_commit(update_query)
	
#------------------------------------------------------------------------------------------
# Stowrzenie tabli z nieustalonuymi punktami i przypisanymi do nich dzialkami  
def crate_pt_dz(): 
	drop_query = "DROP TABLE IF EXISTS nieust_punkty_dzialki;"
	exec_query_commit(drop_query)
	create_query = "CREATE TABLE nieust_punkty_dzialki (ogc_fid INT , dzialka character varying(1500))"
	exec_query_commit(create_query)

	select_query = "select ogc_fid , nr_dzialek from punkty_nieustalone_b002 where nr_dzialek is not null"
	cur.execute(select_query)
	rows = cur.fetchall() 
	for row in rows: 
		ogc_fid = row[0]
		dzilaki = row[1].split(',')
		for dzialka in dzilaki:
			#print str(ogc_fid) + '- ' +dzialka 
			insert_query = "insert into nieust_punkty_dzialki VALUES ('"+str(ogc_fid)+"','"+ dzialka + "');"
			exec_query_commit(insert_query)
	alter_query = "alter table nieust_punkty_dzialki add id serial ;"
	exec_query_commit(alter_query)

#------------------------------------------------------------------------------------------
def crate_dzialki_pary():
	drop_query = "DROP TABLE IF EXISTS id_dzialki_pary;"
	exec_query_commit(drop_query)
	create_query = "CREATE TABLE id_dzialki_pary (id1 INT , id2 INT)"
	exec_query_commit(create_query)
	select_query = "select distinct ogc_fid from nieust_punkty_dzialki"
	cur.execute(select_query)
	rows = cur.fetchall() 
	#petata po ogc_fid punktow 
	for row in rows: 
		ogc_fid  = 	row[0]
		select_query = "select dzialka, id from nieust_punkty_dzialki where ogc_fid ="+str(ogc_fid)+";"
		cur_2.execute(select_query)
		rows_2 = cur_2.fetchall() 
		#szukanie dzialek dla danego punktu 
		for row_2 in rows_2:
			#print row_2
			id =  row_2[1]
			select_query = "select id from nieust_punkty_dzialki where ogc_fid ="+str(ogc_fid)+" and id >"+str (id) +";"
			
			cur_2.execute(select_query)
			rows_3 = cur_2.fetchall() 
			for row_3 in rows_3:
				id_2 = row_3[0]	
				print (str (id) + ' - ' + str (id_2))
				insert_query = "insert into id_dzialki_pary VALUES ('"+str (id)+"','"+ str (id_2) + "');"
				exec_query_commit(insert_query)
	
	drop_query = "DROP TABLE IF EXISTS dzialki_pary"
	exec_query_commit(drop_query)
	create_query = "create table dzialki_pary as (SELECT (SELECT dzialka from nieust_punkty_dzialki A where A.id = B.id1) as dzialka_A, (SELECT dzialka from nieust_punkty_dzialki A where A.id = B.id2) as dzialka_B from id_dzialki_pary B)"

	exec_query_commit(create_query)
	
	#*--------------------------
	'''alter_query = "alter table dzialki_pary add G_dz_a varchar;"
	exec_query_commit(alter_query)
	alter_query = "alter table dzialki_pary add G_dz_b varchar;"
	exec_query_commit(alter_query)

	update_query = "update dzialki_pary A set G_dz_a =(SELECT DISTINCT grupa from dzialki_porabka B where A.dzialka_a like B.nr_dzialki)"
	exec_query_commit(update_query)
	update_query = "update dzialki_pary A set G_dz_b =(SELECT DISTINCT grupa from dzialki_porabka B where A.dzialka_b like B.nr_dzialki)"
	exec_query_commit(update_query)
	
	alter_query = "alter table dzialki_pary add id serial;"
	exec_query_commit(alter_query)
	'''

#stworzenie tabeli z dzialka i grupa nielazleznie do tego czy dzialka posiada adres  
	
	drop_query = "drop table if exists ADRESY_G_All;"
	exec_query_commit(drop_query)
	create_query = "create table ADRESY_G_All as select G, kerg_dz as dz from adresy_g_ok_miej_i_styk union all select G, kerg_dz as dz from adresy_g_BIP_miej_i_styk"
	exec_query_commit(create_query)

	alter_query = "alter table dzialki_pary add G_dz_a varchar;"
	exec_query_commit(alter_query)
	alter_query = "alter table dzialki_pary add G_dz_b varchar;"
	exec_query_commit(alter_query)

	update_query = "update dzialki_pary A set G_dz_a =(SELECT DISTINCT G from ADRESY_G_All B where A.dzialka_a like B.dz)"
	exec_query_commit(update_query)
	update_query = "update dzialki_pary A set G_dz_b =(SELECT DISTINCT G from ADRESY_G_All B where A.dzialka_b like B.dz)"
	exec_query_commit(update_query)
	
	alter_query = "alter table dzialki_pary add id serial;"
	exec_query_commit(alter_query)

def generuj_pliki_csv():

	cur_local_select = conn_PG.cursor()
	# Ci sami wlasciciele brak w skr 
	csw_b_wskr = open('__csv\\csw_b_wskr'+naz_lik_log+'.csv', 'w')
	csw_b_wskr.write ('D1;D2;G1;G2\n')
	select_query = "select distinct *from dzialki_pary where id not in (select distinct B.id from skr A, dzialki_pary B where (A.D1=B.dzialka_a and A.D2=B.dzialka_B) OR (A.D2=B.dzialka_a and A.D1=B.dzialka_B)) and g_dz_a = g_dz_b"
	cur_local_select.execute(select_query) 
	for row in cur_local_select.fetchall():
		csw_b_wskr.write (str(row[0])+';'+ str(row[1])+';'+str(row[2])+';'+str(row[3])+'\n')
	
	# rozni wlasciciele brak w skr 
	rw_b_wskr = open('__csv\\rw_b_wskr'+naz_lik_log+'.csv', 'w')
	rw_b_wskr.write ('D1;D2;G1;G2;Stanowisko\n')
	
	drop_query = "drop table if exists rw_b_wskr;"
	exec_query_commit(drop_query)
	create_query = "create table rw_b_wskr as (select DISTINCT dzialka_a, dzialka_b, g_dz_a, g_dz_b,(SELECT string_agg(DISTINCT nr_stanowiska,'-') from dziakli_miej_z_styk CC where CC.nr_dzialki = AA.dzialka_a ) AS stanowisko from dzialki_pary  AA where id not in (select distinct B.id from skr A, dzialki_pary B where (A.D1=B.dzialka_a and A.D2=B.dzialka_B) OR (A.D2=B.dzialka_a and A.D1=B.dzialka_B)) and (g_dz_a <> g_dz_b or g_dz_a is null or g_dz_b is null ) and (char_length(dzialka_a)<13 OR char_length(dzialka_b)<13))" 
	exec_query_commit(create_query)
	update_query = "update rw_b_wskr A set stanowisko = (SELECT DISTINCT nr_stanowiska from dziakli_miej_z_styk B where B.nr_dzialki = A.dzialka_b) where stanowisko like '';" 
	update_query = "update rw_b_wskr A set stanowisko = (SELECT DISTINCT nr_stanowiska from dziakli_miej_z_styk B where B.nr_dzialki = A.dzialka_b) where stanowisko is null;" 
	exec_query_commit(update_query)
	select_query = "select distinct *from rw_b_wskr;"
	cur_local_select.execute(select_query) 
	for row in cur_local_select.fetchall():
		rw_b_wskr.write (str(row[0])+';'+ str(row[1])+';'+str(row[2])+';'+str(row[3])+';'+str(row[4])+'\n')
		

	# Ci sami wlasciciele sa w skr 
	csw_j_wskr = open('__csv\\csw_j_wskr'+naz_lik_log+'.csv', 'w')
	select_query = "select distinct *from dzialki_pary where id in (select distinct B.id from skr A, dzialki_pary B where (A.D1=B.dzialka_a and A.D2=B.dzialka_B) OR (A.D2=B.dzialka_a and A.D1=B.dzialka_B)) and g_dz_a = g_dz_b"
	cur_local_select.execute(select_query) 
	csw_j_wskr.write ('D1;D2;G1;G2\n')
	for row in cur_local_select.fetchall():
		csw_j_wskr.write (str(row[0])+';'+ str(row[1])+';'+str(row[2])+';'+str(row[3])+'\n')
		
		
	# Rozni wlasciciele sa w skr 
	rw_j_wskr = open('__csv\\rw_j_wskr'+naz_lik_log+'.csv', 'w')
	select_query = "select distinct dzialka_a, dzialka_b, g_dz_a, g_dz_b from dzialki_pary where id in (select distinct B.id from skr A, dzialki_pary B where (A.D1=B.dzialka_a and A.D2=B.dzialka_B) OR (A.D2=B.dzialka_a and A.D1=B.dzialka_B)) and g_dz_a <> g_dz_b"
	rw_j_wskr.write ('D1;D2;G1;G2\n')
	cur_local_select.execute(select_query) 
	for row in cur_local_select.fetchall():
		rw_j_wskr.write (str(row[0])+';'+ str(row[1])+';'+str(row[2])+';'+str(row[3])+'\n')

#---------------------------------------------------------------------------------------------
def create_table_skr(): 
	drop_query = "DROP TABLE IF EXISTS skr;"
	exec_query_commit(drop_query)
	create_query = "CREATE TABLE skr (D1 character varying(100),D2 character varying(100),S character varying(100))"
	exec_query_commit(create_query)
#---------------------------------------------------------------------------------------------
def 	raad_csv():
	with open("skr.skr", 'r') as data_file:
		reader = csv.reader(data_file, delimiter=';')       
		for row in reader:
			D1=row[0]
			D2=row[1]
			S=row[2]
			load_data_2_skr (D1,D2,S)		
#---------------------------------------------------------------------------------------------			
def load_data_2_skr (D1,D2,S):
	insert_query = "insert into skr VALUES ('"+str (D1)+"','"+ str (D2) +"','"+ str (S) +"');"	
	exec_query_commit(insert_query)

#---------------------------------------------------------------------------------------------			
def pomocnicze ():

# stworzenie tabeli z numerami dzialek i grup wlascicieli dla analizowanej miejcowosci i dzilek stykowych dla ktorych sa adresy 

	drop_query = "drop table if exists adresy_g_ok_miej_i_styk;"	
	exec_query_commit(drop_query)

	create_query = """create table adresy_g_ok_miej_i_styk as 
select kerg_dz, g from ADRESY_G_OK_STYK union all 
select dz as kerg_dz,g from ADRESY_G_OK;"""
	exec_query_commit(create_query)	


# stworzenie tabeli z numerami dzialek i grup wlascicieli dla analizowanej miejcowosci i dzilek stykowych idacych na BIP 
	drop_query = "drop table if exists adresy_g_BIP_miej_i_styk;"	
	exec_query_commit(drop_query)

	create_query = """create table adresy_g_BIP_miej_i_styk as 
select kerg_dz, g from ADRESY_G_BIP_STYK union all 
select dz as kerg_dz,g from ADRESY_G_BIP;"""
	exec_query_commit(create_query)	

# stworzenie tabeli z numerami dzialek i grup wlascicieli dla analizowanej miejcowosci i dzilek stykowych idacych na BIP 
	drop_query = "alter table punkty_nieustalone_b002 drop if exists nr_dzialek;"	
	exec_query_commit(drop_query)
	
	add_query = "alter table punkty_nieustalone_b002 add nr_dzialek character varying(2000);;"	
	exec_query_commit(add_query)

	update_query = """update punkty_nieustalone_b002 A set nr_dzialek = (select string_agg(nr_dzialki, ',') from dziakli_miej_z_styk B where St_Intersects (B.wkb_geometry, A.wkb_geometry));"""
	exec_query_commit(update_query)	

#--------------------------------------------------------------------------------------------------------------------------------------------
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#--------------------------------------------------------------------------------------------------------------------------------------------

naz_lik_log = time.strftime("%Y%m%d-%H_%M_%S")
if not os.path.exists('.\\__log'):
    try:
        os.makedirs('.\\__log')
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

logfile = open('__log\\'+naz_lik_log+'.log', 'w')
err_log = open('__log\\ERR'+naz_lik_log+'.log', 'w')

main_dir = os.getcwd()

teraz = time.asctime( time.localtime(time.time()))
try:
	conn_PG = psycopg2.connect("dbname='__dbname__' user='__user__' host='__host__' password='__passwd__' port='5432'")
	logfile.write(teraz + ' [INF] Polaczono z baza danych\n')
except:
	print ('I am unable to connect to the database')
	err_log.write(teraz +' - [ERR] Nie udalo sie naiazac polacznia z baz\n')

cur = conn_PG.cursor()
cur_2 = conn_PG.cursor()

# pobranie z xls danych adresowych dla dzialek 

create_table_skr()
raad_csv()
get_dresy()
get_dresy_stykowe()
pomocnicze ()
crate_pt_dz()
crate_dzialki_pary()
generuj_pliki_csv()




#insert_query = "insert into nieust_punkty_dzialki VALUES ('"+str(ogc_fid)+"','"+ dzialka + "');"
#exec_query_commit(insert_query)
		
	
os.system("pause")