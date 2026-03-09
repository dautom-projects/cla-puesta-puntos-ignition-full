#* DAUTOM SAS CONFIDENTIAL 
#*_________________________ 
#* 
#* [2013] - [2024] DAUTOM SAS 
#* All Rights Reserved. 
#* 
#* NOTICE: All information contained herein is, and remains the property 
#* of DAUTOM SAS and its suppliers, if any. The intellectual and  
#* technical concepts contained herein are proprietary to DAUTOM SAS 
#* and its suppliers and may be covered by U.S and Foreign Patents,  
#* patents in process, and are protected by trade secret or copyright law.
#* Dissemination of this information or reproduction of this material 
#* is scrictly forbidden unless prior written permission is obtained 
#* from DAUTOM SAS.

import time
import re
import datetime
import os

#logger = system.util.getLogger("Save Temp Pasteu Report")
currentDateTime = system.date.now()
# currentDateTime = system.date.getDate(2025, 1, 20)  # Mes en base 0, por eso febrero es 1
currentDateTime = system.date.midnight(currentDateTime)  # 00:00:00 hoy
currentDateTime = system.date.addHours(currentDateTime, 5)  # 05:00:00
currentDateTime = system.date.addSeconds(currentDateTime, 59 * 60 + 59)  # 05:59:59

# *** FIX principal: usar -1 día para que start < end (ayer 06:00:00 -> hoy 05:59:59)
startDateTime = system.date.addSeconds(system.date.addDays(currentDateTime, -1), 1)

#
system.tag.writeBlocking("[default]/Bogota/Report_Temperature_Pasteu/startDateTime", startDateTime)
logger.info("Start Time: {}".format(startDateTime))
system.tag.writeBlocking("[default]/Bogota/Report_Temperature_Pasteu/EndDateTime", currentDateTime)
logger.info("End Time: {}".format(currentDateTime))

date = startDateTime
year = system.date.getYear(date)
month = system.date.getMonth(date) + 1 
day = system.date.getDayOfMonth(date)

# Format month/day as two digits
month_str = str(month).zfill(2)
day_str = str(day).zfill(2)

# "YYYY-MM-DD"
formatted_date = "{}-{}-{}".format(year, month_str, day_str)


fileDirectory = "C:\\Users\\Administrador\\Documents\\Reportes\\Reporte Temperatura Pasteutizacion"
directory = r"{}\{}".format(fileDirectory, formatted_date)
#logger.info("Directory: {}".format(directory))

# Crear carpeta si no existe
if not os.path.exists(directory):
    os.makedirs(directory)


try:
    # Dejo tu patrón con writeBlocking
    system.tag.writeBlocking("[default]/Bogota/Report_Temperature_Pasteu/Line", line)
    time.sleep(10)

    params = {"refresh": system.tag.readBlocking("[default]/Bogota/Report_Temperature_Pasteu/Refresh")[0].value}

    pdfBytes = system.report.executeReport(
        path="Temperature_past_line_0{}".format(line),
        project="ignitionapps",
        parameters=params,
        fileType="pdf"
    )

    fileName = "REPORTE_TEMPERATURAS_PASTEURIZACION_LINEA_0{}_{}".format(line, formatted_date)
    pdf_path = "{}\\{}.pdf".format(directory, fileName)
    #logger.info("pdf_path: {}".format(pdf_path))

    with open(pdf_path, "wb") as f:
        f.write(pdfBytes)

    #logger.info("saved pdf for line {}".format(line))

except Exception as e:
    #logger.error("line {} failed: {}".format(line, e))
    None







#* DAUTOM SAS CONFIDENTIAL
#*_________________________
#*
#* [2013] - [2024] DAUTOM SAS
#* All Rights Reserved.
#*
#* NOTICE: All information contained herein is, and remains the property
#* of DAUTOM SAS and its suppliers, if any. The intellectual and 
#* technical concepts contained herein are proprietary to DAUTOM SAS
#* and its suppliers and may be covered by U.S and Foreign Patents, 
#* patents in process, and are protected by trade secret or copyright law. 
#* Dissemination of this information or reproduction of this material
#* is scrictly forbidden unless prior written permission is obtained
#* from DAUTOM SAS. 

"""
Handles the scheduled event to send a process control report via email.
This function:
1. Retrieves the current date and time.
2. Adjusts the date to be one day earlier.
3. Formats the date and time components to ensure they have two digits.
4. Constructs an email with the formatted date in the subject.
5. Sends the email with the attached report.
Imports:
    datetime: For handling date and time operations.
Uses:
    report.sendReportEmails: To send the email with the report attached.
"""
import datetime

# Get the current date and time, then subtract one day
timeNow = datetime.datetime.now()
currentDateTime = timeNow - datetime.timedelta(days=1)
year = currentDateTime.year
month = currentDateTime.month
day = currentDateTime.day
hour = currentDateTime.hour
minute = currentDateTime.minute

# Ensure month, day, hour, and minute are two digits
month_str = str(month).zfill(2)
day_str = str(day).zfill(2)
hour_str = str(hour).zfill(2)
min_str = str(minute).zfill(2)

# Format the date as "YYYY-MM-DD" and time as "-HHMM"
formatted_date = "{}-{}-{}".format(year, month_str, day_str)
formatted_time = "-{}{}".format(hour_str, min_str)

# Email details
smtpProfile = "email-team"
fromAddr = "ignition_team@outlook.com"
subject = "Reporte control de proceso Linea 07 {}".format(formatted_date)
body = """Buenos dias,\n\nSe envia adjunto el control de proceso de la linea 07 del dia {}.\n\nAtentamente,\n\n\nFactory Compass\nEfficiency Management System""".format(formatted_date)
recipients = [
    ""
]
fileDirectory = "C:\\Users\\Administrador\\Documents\\Reportes\\Linea07"

# Send the report via email
report.sendReportEmails(smtpProfile, fromAddr, subject, body, recipients, fileDirectory)
 