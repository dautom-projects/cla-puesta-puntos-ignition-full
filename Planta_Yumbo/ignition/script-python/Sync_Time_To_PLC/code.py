# Importar el módulo datetime
import datetime

# Obtener la fecha y hora actual
now = datetime.datetime.now()

# Obtener el año, mes, día, hora, minutos y segundos actuales
ano = now.year


# Escribir los valores en tags del PLC
system.tag.write("[default]Ensamble/LINEA 1/TERMOSELLADORA L1/Sync_Time_From_Server/Sync_Time_From_Server_0_, value", ano)

