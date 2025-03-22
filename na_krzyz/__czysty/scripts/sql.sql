drop table if exists punkty;

drop table if exists dzialki_Rawalowice_0017;
create table dzialki_Rawalowice_0017 as 
select dnr as nr_dzialki, ''::varchar  as nr_stanowiska, ''::varchar as grupa,wkb_geometry FROM dzialki;

--***************************************************************************
drop table if exists stanowiska;
create table stanowiska as select *from punkty where level = 56;
delete from stanowiska where ogc_fid in (
select A.ogc_fid from stanowiska A, stanowiska B where  st_equals (A.wkb_geometry,B.wkb_geometry) and A.ogc_fid > B.ogc_fid and A.text like B.text) --and operat = 1;
-- dodanie numerow stanowisk nawet jesli podwujne 
update dzialki_Rawalowice_0017 A set nr_stanowiska = (select string_agg(distinct text, ' - ') from stanowiska B where ST_Within( B.wkb_geometry, A.wkb_geometry));
-- kontrola czy sa jeszcze podwujne jak tak poprawka 
select *from dzialki_Rawalowice_0017 where nr_stanowiska like '%-%';

-- poprawa blednych 
update dzialki_Rawalowice_0017 A set nr_stanowiska = '02B15' where nr_stanowiska = '02B15 - 02C16';


-- stworzenie tabli z liniami dla danego obrebu 
drop table if exists lnie_garanic_ustalenia_obr;
create table lnie_garanic_ustalenia_obr as select distinct A.* from lnie_garanic_ustalenia A, dzialki_Rawalowice_0017 B where ST_Within(A.wkb_geometry , st_buffer (B.wkb_geometry,0.02)) and length(nr_dzialki) < 12


-- stworzenei tabeli z punktami nie ustalonymi 
drop table if exists punkty_nieustalone;
create table punkty_nieustalone as 
select distinct A.* from punkty_graniczne_pot A, lnie_garanic_ustalenia_obr B  where st_intersects (st_buffer (A.wkb_geometry,0.2),B.wkb_geometry) ;


--***************************************************************************
-- stworzenie tabeli z dziaklami z buforem dla analizowanej amiejcowoci 
alter table dzialki_Rawalowice_0017 add ogc_fid serial;
drop table if exists dzialki_poligony_buf01;
create table dzialki_poligony_buf01 as 
select ogc_fid, st_buffer (wkb_geometry, '0.1') as wkb_geometry from dzialki_Rawalowice_0017 where length(nr_dzialki) < 12  ;


-- stworzenie tabeli z dzialkami stykowymi dla analizowanej miejcowosci 
drop table if exists dzialki_styk; 
create table dzialki_styk as 
select DISTINCT A.* from dzialki_Rawalowice_0017 A, dzialki_poligony_buf01 B where st_intersects(A.wkb_geometry, B.wkb_geometry) and A.ogc_fid not in (
select ogc_fid from dzialki_poligony_buf01
);

-- stworzenie tebeli zawierajacej dzialki z analizowanej miejcowosci i dzialkami stykowymi 
drop table if exists dziakli_miej_z_styk;
create table dziakli_miej_z_styk as 
select wkb_geometry, nr_dzialki, '' as nr_stanowiska from dzialki_styk union all 
select wkb_geometry, nr_dzialki, nr_stanowiska from dzialki_Rawalowice_0017 where ogc_fid in (select ogc_fid from dzialki_poligony_buf01);

--***************************************************************************

-- punkty nieustalone z buforem 
drop table if exists punkty_nieustalone_b002; 
create table punkty_nieustalone_b002 as select ogc_fid , st_buffer (wkb_geometry,'0.02') as wkb_geometry from punkty_nieustalone;

alter table punkty_nieustalone_b002 drop if exists  nr_dzialek;
alter table punkty_nieustalone_b002 add nr_dzialek character varying(200);
update punkty_nieustalone_b002 A set nr_dzialek = (select string_agg(nr_dzialki, ',') from dziakli_miej_z_styk B where St_Intersects (B.wkb_geometry, A.wkb_geometry));



!!!!!!!!-- puścic skrypt 

-- stworzenie tabeli z numerami dzialek i grup wlascicieli dla analizowanej miejcowosci i dzilek stykowych dla ktorych sa adresy 
drop table if exists adresy_g_ok_miej_i_styk;
create table adresy_g_ok_miej_i_styk as 
select kerg_dz, g from ADRESY_G_OK_STYK union all 
select dz as kerg_dz,g from ADRESY_G_OK;

-- stworzenie tabeli z numerami dzialek i grup wlascicieli dla analizowanej miejcowosci i dzilek stykowych idacych na BIP 
drop table if exists adresy_g_BIP_miej_i_styk;
create table adresy_g_BIP_miej_i_styk as 
select kerg_dz, g from ADRESY_G_BIP_STYK union all 
select dz as kerg_dz,g from ADRESY_G_BIP;


alter table punkty_nieustalone_b002 drop nr_dzialek;
alter table punkty_nieustalone_b002 add nr_dzialek character varying(2000);
update punkty_nieustalone_b002 A set nr_dzialek = (select string_agg(nr_dzialki, ',') from dziakli_miej_z_styk B where St_Intersects (B.wkb_geometry, A.wkb_geometry));



--************************************************************************************
-- kontrola i generowanei po poprawkach 
select distinct dzialka_a, dzialka_b, g_dz_a, g_dz_b from dzialki_pary where id in (select distinct B.id from skr A, dzialki_pary B where (A.D1=B.dzialka_a and A.D2=B.dzialka_B) OR (A.D2=B.dzialka_a and A.D1=B.dzialka_B)) and g_dz_a <> g_dz_b

select *from rw_b_wskr;
select *from skr
delete from skr where d1 like 'D1'

drop table dziki_pary_por
create table dziki_pary_por as 
select dzialka_a, dzialka_b from rw_b_wskr union all 
select d1,d2 from skr 

select *from Rawalowice_0017_dz_bez_duble A where dz_1||dz_2 not in (select dzialka_a||dzialka_b from dziki_pary_por) AND dz_2||dz_1 not in (select dzialka_a||dzialka_b from dziki_pary_por) --72

create table skr_Rawalowice_0017 as 
select dz_1, dz_2, wartosc from Rawalowice_0017_dz_bez_duble A where dz_1||dz_2 in (select dzialka_a||dzialka_b from dziki_pary_por) OR dz_2||dz_1 in (select dzialka_a||dzialka_b from dziki_pary_por) --4477 


alter table skr_Rawalowice_0017 add s varchar;
update skr_Rawalowice_0017 A set s = (SELECT B.s from skr B where B.d1||B.d2 like A.dz_1||A.dz_2 or B.d2||B.d1 like A.dz_1||A.dz_2)
update skr_Rawalowice_0017 A set s = (SELECT distinct B.stanowisko from rw_b_wskr B where B.dzialka_a||B.dzialka_b like A.dz_1||A.dz_2 or B.dzialka_b||B.dzialka_a like A.dz_1||A.dz_2) where s is null 

select dz_1, dz_2, s from skr_Rawalowice_0017 where s is null 
select *from rw_b_wskr 
select *from skr 


