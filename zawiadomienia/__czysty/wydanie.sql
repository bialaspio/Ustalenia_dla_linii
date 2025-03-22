-- kontrola czy brak null-i 
select *from ZAWIADOMIENIA where adr_cz2_pop is null ;
-- adresy BIP
select DATA,GODZINA,G,DDD,KW,WL,RODZICE,adr_cz2_pop as ADRES_CZ2,adr_cz1_pop AS ADRES_CZ1, pwpt from ZAWIADOMIENIA where adr_cz2_pop like 'BIP';
-- adresy na OK
select DATA,GODZINA,G,DDD,KW,WL,RODZICE,adr_cz2_pop as ADRES_CZ2,adr_cz1_pop AS ADRES_CZ1, pwpt from ZAWIADOMIENIA where adr_cz2_pop not like 'BIP';

