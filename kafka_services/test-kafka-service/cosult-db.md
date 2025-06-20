## Consultas para la base de datos sistema_monitoreo

## Consulta para extraer datos de una tabla

Acontinuacion se listaran todas las consultas necesarias para extraer la data de una tabla de db:

Nota: Cuando la base de datos se llene con los nombres reales hay que reemplzar los datos de las consultas con el nombre de la variable que se desea seleccioanr la data. Ej: channel_10 se reemplaza por potencia_aparente.

- Mostrar la ultima fila de una tabla:
  SELECT \* FROM fgenerador1_data ORDER BY id DESC LIMIT 1;

- Motrar una variable en especifico son su respectivo valor:
  SELECT name_10, channel_10 FROM fgenerador1_data ORDER BY id DESC LIMIT 1;

- Mostrar un grupo de variables basado en las agrupaciones de variables de fuel monitoring (Caso de Lubrication detais):
  SELECT
  name_01, channel_01,
  name_02, channel_02,
  name_03, channel_03,
  name_04, channel_04,
  name_05, channel_06,
  FROM fgenerador1_data ORDER BY id DESC LIMI1;
