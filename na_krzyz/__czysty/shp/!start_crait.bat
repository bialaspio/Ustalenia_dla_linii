@echo off
set OSGEO4W_ROOT=C:\Program Files\QGIS 2.18
PATH=%OSGEO4W_ROOT%\bin;%PATH%
for %%f in (%OSGEO4W_ROOT%\etc\ini\*.bat) do call %%f
@echo on

set PGCLIENTENCODING=WIN1250
set host=__host__
set label=ID


for %%I in (*.shp) do (
ogr2ogr -f "PostgreSQL" "PG:dbname=__db_name__ user=__user__ password=__passwd__ host=%host% port=5432" %%I -nln %%~nI -nlt GEOMETRY
)

pause	