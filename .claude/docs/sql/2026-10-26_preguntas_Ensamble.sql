-- Preguntas fijas de los formularios -> papoitem.Description
-- Generado por papo_objects.py --questions-sql el 2026-10-26: el formulario lee la pregunta de papoItemID y
-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en produccion.

SET XACT_ABORT ON;
BEGIN TRANSACTION;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Verificacion dimensional de la placa con galga segun procedimiento Manejo de galgas EA12-0300'
UPDATE papoitem SET Description = N'Verificacion dimensional de la placa con galga segun procedimiento Manejo de galgas EA12-0300' WHERE ID = 280;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Verificacion de atributos de placa Positiva segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.'
UPDATE papoitem SET Description = N'Verificacion de atributos de placa Positiva segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.' WHERE ID = 281;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Verificacion de atributos de placa Negativa segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.'
UPDATE papoitem SET Description = N'Verificacion de atributos de placa Negativa segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.' WHERE ID = 282;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Funcionamiento del balancin de tension del rollo (Estado de lubricacion y movimiento libre sin atasques)'
UPDATE papoitem SET Description = N'Funcionamiento del balancin de tension del rollo (Estado de lubricacion y movimiento libre sin atasques)' WHERE ID = 287;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Placa negativa sin deformacion despues de ensobrada'
UPDATE papoitem SET Description = N'Placa negativa sin deformacion despues de ensobrada' WHERE ID = 292;
-- Page/Embedded/Ensamble/Form_EA11-1101_1h  antes: N'Bateria referencia Sofasa, segregar los primeros 50 cm del rollo y ubicarlos en el anaquel'
UPDATE papoitem SET Description = N'Bateria referencia Sofasa, segregar los primeros 50 cm del rollo y ubicarlos en el anaquel' WHERE ID = 293;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5s'
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5''s.' WHERE ID = 258;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Cabinas electricas cerradas'
UPDATE papoitem SET Description = N'Cabinas electricas cerradas.' WHERE ID = 259;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Guardas en su lugar'
UPDATE papoitem SET Description = N'Guardas en su lugar.' WHERE ID = 260;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Cabinas electricas con libre acceso'
UPDATE papoitem SET Description = N'Cabinas electricas con libre acceso.' WHERE ID = 261;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena'
UPDATE papoitem SET Description = N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena' WHERE ID = 262;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'No hay objetos sobre las cabinas electicas'
UPDATE papoitem SET Description = N'No hay objetos sobre las cabinas electicas.' WHERE ID = 263;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Cableado en buenas condiciones'
UPDATE papoitem SET Description = N'Cableado en buenas condiciones.' WHERE ID = 264;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Switch y controles de seguridad funcionando correctamente'
UPDATE papoitem SET Description = N'Switch y controles de seguridad funcionando correctamente.' WHERE ID = 265;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'No hay fugas ni goteos en las maquinas'
UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas.' WHERE ID = 266;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Boton parada de emergencia funcionando correctamente'
UPDATE papoitem SET Description = N'Boton parada de emergencia funcionando correctamente.' WHERE ID = 267;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Buen estado y tension de las cadenas, pinones y bandas'
UPDATE papoitem SET Description = N'Buen estado y tension de las cadenas, pinones y bandas' WHERE ID = 269;
-- Page/Embedded/Ensamble/Form_EA11-1101_start  antes: N'Se encuentran calibrados los elementos de medicion'
UPDATE papoitem SET Description = N'Se encuentran calibrados los elementos de medicion' WHERE ID = 272;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Penetracion bandera hombro'
UPDATE papoitem SET Description = N'Penetracion bandera hombro' WHERE ID = 341;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Aplicacion de flux en bandera.'
UPDATE papoitem SET Description = N'Aplicacion de flux en bandera' WHERE ID = 343;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Alineacion de bandera - hombro.'
UPDATE papoitem SET Description = N'Alineacion de bandera - hombro' WHERE ID = 347;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Frecuencia segun plan control EA07-0300'
UPDATE papoitem SET Description = N'Frecuencia segun plan control EA07-0300' WHERE ID = 2017;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Espesor de hombro.'
UPDATE papoitem SET Description = N'Espesor de hombro' WHERE ID = 342;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Estado de banderas segun plan control EA07-0300.'
UPDATE papoitem SET Description = N'Estado de banderas segun plan control EA07-0300' WHERE ID = 344;
-- Page/Embedded/Ensamble/Form_EA11-2201_1h  antes: N'Condicion del strap segun plan control EA07-0300.'
UPDATE papoitem SET Description = N'Condicion del strap segun plan control EA07-0300' WHERE ID = 346;
-- Page/Embedded/Ensamble/Form_EA11-2201_2h  antes: N'No Cristalizacion ni fractura de espigos y hombros segun plan control EA07-0300.'
UPDATE papoitem SET Description = N'No Cristalizacion ni fractura de espigos y hombros segun plan control EA07-0300' WHERE ID = 349;
-- Page/Embedded/Ensamble/Form_EA11-2201_start  antes: N'aArea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.'
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5''s.' WHERE ID = 312;
-- Page/Embedded/Ensamble/Form_EA11-2201_start  antes: N'Guardas, switch y controles de seguridad funcionando correctamente..'
UPDATE papoitem SET Description = N'Guardas, switch y controles de seguridad funcionando correctamente.' WHERE ID = 314;
-- Page/Embedded/Ensamble/Form_EA11-2201_start  antes: N'No hay fugas ni goteos en las maquinas'
UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas.' WHERE ID = 318;
-- Page/Embedded/Ensamble/Form_EA11-2201_start  antes: N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena.'
UPDATE papoitem SET Description = N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena.' WHERE ID = 319;
-- Page/Embedded/Ensamble/Form_EA11-2501_30min  antes: N'Prueba de desgarre soldadura de punto cada 30 minutos, revisar criterios de Aceptacion y Rechazo.'
UPDATE papoitem SET Description = N'Prueba de desgarre soldadura de punto cada 30 minutos, revisar criterios de Aceptacion y Rechazo' WHERE ID = 3093;
-- Page/Embedded/Ensamble/Form_EA11-2501_30min  antes: N'Alineacion de soldadura.'
UPDATE papoitem SET Description = N'Alineacion de soldadura' WHERE ID = 3095;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.'
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5''s.' WHERE ID = 3054;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'No hay fugas ni goteos en las maquinas'
UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas.' WHERE ID = 3061;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Los electrodos de prueba se encuentra en buen estado.'
UPDATE papoitem SET Description = N'Los electrodos de prueba se encuentran en buen estado.' WHERE ID = 3062;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Electrodos en buen estado segun criterios de aceptacion y rechazo.'
UPDATE papoitem SET Description = N'Electrodos en buen estado segun criterio de aceptacion y rechazo' WHERE ID = 3067;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'El cableado electrico esta bien conectado.'
UPDATE papoitem SET Description = N'El cableado electrico esta bien conectado.' WHERE ID = 3063;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Electrodos, mordazas, aislante y correas limpias, secas, en buen estado alineados y ajustados..'
UPDATE papoitem SET Description = N'Electrodos, mordazas, aislante y correas limpias, secas, en buen estado alineados y ajustados.' WHERE ID = 3068;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'La estacion de rechazo se encuentra operando adecuadamente.'
UPDATE papoitem SET Description = N'La estacion de rechazo se encuentra operando adecuadamente' WHERE ID = 3064;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'El nivel de aceite en la unidad de mantenimiento se encuentra bien.'
UPDATE papoitem SET Description = N'El nivel de aceite en la unidad de mantenimiento se encuentra bien' WHERE ID = 3069;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Los instrumentos de medicion se encuentran calibrados.'
UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados.' WHERE ID = 3066;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Los instrumentos de medicion se encuentran calibrados.'
UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados.' WHERE ID = 3072;
-- Page/Embedded/Ensamble/Form_EA11-2501_start  antes: N'Tornilleria bien ajustada y en buen estado.'
UPDATE papoitem SET Description = N'Tornilleria bien ajustada y en buen estado.' WHERE ID = 3073;
-- Page/Embedded/Ensamble/Form_EA11-2601_2h  antes: N'Peso Hotmelt (Bat. 31: 80 +/- 10 gr/Bat. Bat. 4D-4DLT y 8D: 150 +/- 10 gr/Bat)'
UPDATE papoitem SET Description = N'Peso Hotmelt (Bat. 31 (80 +/- 10 gr/Bat) Bat. 4D-4DLT y 8D ( 150+/- 10 gr/Bat)' WHERE ID = 11352;
-- Page/Embedded/Ensamble/Form_EA11-4101_1h, Page/Embedded/Ensamble/Form_EA11-4101_2h  antes: N'Altura  Espigos acorde especificacion / USE GALGA '
UPDATE papoitem SET Description = N'Altura Espigos acorde especificacion/ USE GALGA' WHERE ID = 3118;
-- Page/Embedded/Ensamble/Form_EA11-4101_2h  antes: N'Medidores de gas y oxigeno de alta en buen estado.'
UPDATE papoitem SET Description = N'Medidores de gas y oxigeno de alta en buen estado.' WHERE ID = 3122;
-- Page/Embedded/Ensamble/Form_EA11-4101_2h  antes: N'Rotametros enfriamiento en buen estado .'
UPDATE papoitem SET Description = N'Rotametros enfriamiento en buen estado.' WHERE ID = 3117;
-- Page/Embedded/Ensamble/Form_EA11-4101_end  antes: N'Buen estado de electrodos ( Cambiar electrodos cada 5000 baterias Fabricadas).'
UPDATE papoitem SET Description = N'Buen estado de electrodos (Cambiar electrodos cada 5000 baterias Fabricadas).' WHERE ID = 3124;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.'
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5''s.' WHERE ID = 3099;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'No hay objetos dentro ni sobre las cabinas electricas.'
UPDATE papoitem SET Description = N'No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 3103;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'No hay fugas ni goteos en las las maquinas.'
UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas.' WHERE ID = 3105;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Switch de seguro de puerta activo .'
UPDATE papoitem SET Description = N'Switch de seguro de puerta activo.' WHERE ID = 3106;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Presion de aire de la linea principal entre SET POINT 95psi - VARIACIaAN PROCESO 85 - 105.'
UPDATE papoitem SET Description = N'Presion de aire de la linea principal entre SET POINT 95 psi' + NCHAR(160) + N' ' + NCHAR(160) + N'- Variacion proceso 85 - 105 psi' WHERE ID = 3107;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Buen estado pantalla de control panel touch .'
UPDATE papoitem SET Description = N'Buen estado pantalla de control panel touch.' WHERE ID = 3108;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'No hay fugas  de  gas y oxigeno.'
UPDATE papoitem SET Description = N'No hay fugas de gas y oxigeno.' WHERE ID = 3113;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Mangueras de Borneadora manual y APB en buen estado, grafadas y con arrestador de llama en la salida.'
UPDATE papoitem SET Description = N'Mangueras de borneadora manual y APB en buen estado, grafadas y con arrestador de llama en salida.' WHERE ID = 3114;
-- Page/Embedded/Ensamble/Form_EA11-4101_start  antes: N'Buen estado del economizador (apague la llama cuando se ubique sobre el).'
UPDATE papoitem SET Description = N'Buen estado del economizador (apague la llama cuando se ubique sobre el).' WHERE ID = 3115;
-- Page/Embedded/Ensamble/Form_EA11-4200_1h, Page/Embedded/Ensamble/Form_EA11-4200_2h, Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Verificacion DAPE con muestra patron'
UPDATE papoitem SET Description = N'Verificacion de DAPE con muestra patron' WHERE ID = 3050;
-- Page/Embedded/Ensamble/Form_EA11-4200_1h, Page/Embedded/Ensamble/Form_EA11-4200_2h, Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Apariencia de bateria (rayada, quemada, golpeada, deformaciones en sellado, etc)'
UPDATE papoitem SET Description = N'Apariencia de bateria (rayada, quemada, golpeada, deformaciones en sellado, etc)' WHERE ID = 3053;
-- Page/Embedded/Ensamble/Form_EA11-4200_2h, Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'No presencia de rebabas'
UPDATE papoitem SET Description = N'No presencia de rebabas.' WHERE ID = 3048;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'aArea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.'
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5''s.' WHERE ID = 3001;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Estibador manual en buen estado.'
UPDATE papoitem SET Description = N'Estibador manual en buen estado' WHERE ID = 3005;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'No hay fugas ni goteos en las maquinas'
UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas.' WHERE ID = 3009;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Todas las resistencias se encuentras en buen estado.'
UPDATE papoitem SET Description = N'Todas las resistencias se encuentran en buen estado' WHERE ID = 3011;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Manometros calibrados y en buen estado.'
UPDATE papoitem SET Description = N'Manometros calibrados y en buen estado' WHERE ID = 3016;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Se encuentran las galgas en el puesto y con calibracion vigente.'
UPDATE papoitem SET Description = N'Se encuentran las galgas en el puesto y con calibracion vigente' WHERE ID = 3012;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Presion de aire alcanza el valor indicado en la prueba.'
UPDATE papoitem SET Description = N'Presion de aire alcanza el valor indicado en la prueba' WHERE ID = 3017;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Los amperimetros estan funcionando.'
UPDATE papoitem SET Description = N'Los amperimetros estan funcionando' WHERE ID = 3013;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'El equipo opera correctamente.'
UPDATE papoitem SET Description = N'El equipo opera correctamente' WHERE ID = 3018;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Inexistencia de ruidos inusuales.'
UPDATE papoitem SET Description = N'Inexistencia de ruidos inusuales' WHERE ID = 3014;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Inexistencia de ruidos inusuales.'
UPDATE papoitem SET Description = N'Inexistencia de ruidos inusuales' WHERE ID = 3019;
-- Page/Embedded/Ensamble/Form_EA11-4200_start  antes: N'Los instrumentos de medicion se encuentran calibrados.'
UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados' WHERE ID = 3015;
COMMIT;

-- Rollback:
-- UPDATE papoitem SET Description = N'Verificacion dimensional de la placa con galga segun procedimiento Manejo de galgas EA12-0300' WHERE ID = 280;
-- UPDATE papoitem SET Description = N'Verificacion de atributos de placa Positiva segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.' WHERE ID = 281;
-- UPDATE papoitem SET Description = N'Verificacion de atributos de placa Negativa segun criterio de aceptacion y rechazos RH02-0500 ANEXO 4.' WHERE ID = 282;
-- UPDATE papoitem SET Description = N'Funcionamiento del balancin de tension del rollo (Estado de lubricacion y movimiento libre sin atasques)' WHERE ID = 287;
-- UPDATE papoitem SET Description = N'Placa negativa sin deformacion despues de ensobrada' WHERE ID = 292;
-- UPDATE papoitem SET Description = N'Bateria referencia Sofasa, segregar los primeros 50 cm del rollo y ubicarlos en el anaquel' WHERE ID = 293;
-- UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5s' WHERE ID = 258;
-- UPDATE papoitem SET Description = N'Cabinas electricas cerradas' WHERE ID = 259;
-- UPDATE papoitem SET Description = N'Guardas en su lugar' WHERE ID = 260;
-- UPDATE papoitem SET Description = N'Cabinas electricas con libre acceso' WHERE ID = 261;
-- UPDATE papoitem SET Description = N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena' WHERE ID = 262;
-- UPDATE papoitem SET Description = N'No hay objetos sobre las cabinas electicas' WHERE ID = 263;
-- UPDATE papoitem SET Description = N'Cableado en buenas condiciones' WHERE ID = 264;
-- UPDATE papoitem SET Description = N'Switch y controles de seguridad funcionando correctamente' WHERE ID = 265;
-- UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas' WHERE ID = 266;
-- UPDATE papoitem SET Description = N'Boton parada de emergencia funcionando correctamente' WHERE ID = 267;
-- UPDATE papoitem SET Description = N'Buen estado y tension de las cadenas, pinones y bandas' WHERE ID = 269;
-- UPDATE papoitem SET Description = N'Se encuentran calibrados los elementos de medicion' WHERE ID = 272;
-- UPDATE papoitem SET Description = N'Penetracion bandera hombro' WHERE ID = 341;
-- UPDATE papoitem SET Description = N'Aplicacion de flux en bandera.' WHERE ID = 343;
-- UPDATE papoitem SET Description = N'Alineacion de bandera - hombro.' WHERE ID = 347;
-- UPDATE papoitem SET Description = N'Frecuencia segun plan control EA07-0300' WHERE ID = 2017;
-- UPDATE papoitem SET Description = N'Espesor de hombro.' WHERE ID = 342;
-- UPDATE papoitem SET Description = N'Estado de banderas segun plan control EA07-0300.' WHERE ID = 344;
-- UPDATE papoitem SET Description = N'Condicion del strap segun plan control EA07-0300.' WHERE ID = 346;
-- UPDATE papoitem SET Description = N'No Cristalizacion ni fractura de espigos y hombros segun plan control EA07-0300.' WHERE ID = 349;
-- UPDATE papoitem SET Description = N'aArea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 312;
-- UPDATE papoitem SET Description = N'Guardas, switch y controles de seguridad funcionando correctamente..' WHERE ID = 314;
-- UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas' WHERE ID = 318;
-- UPDATE papoitem SET Description = N'Verificacion del estado del polipasto y los elementos como cadena, botonera, dispositivos de izaje y bolsa guarda cadena.' WHERE ID = 319;
-- UPDATE papoitem SET Description = N'Prueba de desgarre soldadura de punto cada 30 minutos, revisar criterios de Aceptacion y Rechazo.' WHERE ID = 3093;
-- UPDATE papoitem SET Description = N'Alineacion de soldadura.' WHERE ID = 3095;
-- UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 3054;
-- UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas' WHERE ID = 3061;
-- UPDATE papoitem SET Description = N'Los electrodos de prueba se encuentra en buen estado.' WHERE ID = 3062;
-- UPDATE papoitem SET Description = N'Electrodos en buen estado segun criterios de aceptacion y rechazo.' WHERE ID = 3067;
-- UPDATE papoitem SET Description = N'El cableado electrico esta bien conectado.' WHERE ID = 3063;
-- UPDATE papoitem SET Description = N'Electrodos, mordazas, aislante y correas limpias, secas, en buen estado alineados y ajustados..' WHERE ID = 3068;
-- UPDATE papoitem SET Description = N'La estacion de rechazo se encuentra operando adecuadamente.' WHERE ID = 3064;
-- UPDATE papoitem SET Description = N'El nivel de aceite en la unidad de mantenimiento se encuentra bien.' WHERE ID = 3069;
-- UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados.' WHERE ID = 3066;
-- UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados.' WHERE ID = 3072;
-- UPDATE papoitem SET Description = N'Tornilleria bien ajustada y en buen estado.' WHERE ID = 3073;
-- UPDATE papoitem SET Description = N'Peso Hotmelt (Bat. 31: 80 +/- 10 gr/Bat. Bat. 4D-4DLT y 8D: 150 +/- 10 gr/Bat)' WHERE ID = 11352;
-- UPDATE papoitem SET Description = N'Altura  Espigos acorde especificacion / USE GALGA ' WHERE ID = 3118;
-- UPDATE papoitem SET Description = N'Medidores de gas y oxigeno de alta en buen estado.' WHERE ID = 3122;
-- UPDATE papoitem SET Description = N'Rotametros enfriamiento en buen estado .' WHERE ID = 3117;
-- UPDATE papoitem SET Description = N'Buen estado de electrodos ( Cambiar electrodos cada 5000 baterias Fabricadas).' WHERE ID = 3124;
-- UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 3099;
-- UPDATE papoitem SET Description = N'No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 3103;
-- UPDATE papoitem SET Description = N'No hay fugas ni goteos en las las maquinas.' WHERE ID = 3105;
-- UPDATE papoitem SET Description = N'Switch de seguro de puerta activo .' WHERE ID = 3106;
-- UPDATE papoitem SET Description = N'Presion de aire de la linea principal entre SET POINT 95psi - VARIACIaAN PROCESO 85 - 105.' WHERE ID = 3107;
-- UPDATE papoitem SET Description = N'Buen estado pantalla de control panel touch .' WHERE ID = 3108;
-- UPDATE papoitem SET Description = N'No hay fugas  de  gas y oxigeno.' WHERE ID = 3113;
-- UPDATE papoitem SET Description = N'Mangueras de Borneadora manual y APB en buen estado, grafadas y con arrestador de llama en la salida.' WHERE ID = 3114;
-- UPDATE papoitem SET Description = N'Buen estado del economizador (apague la llama cuando se ubique sobre el).' WHERE ID = 3115;
-- UPDATE papoitem SET Description = N'Verificacion DAPE con muestra patron' WHERE ID = 3050;
-- UPDATE papoitem SET Description = N'Apariencia de bateria (rayada, quemada, golpeada, deformaciones en sellado, etc)' WHERE ID = 3053;
-- UPDATE papoitem SET Description = N'No presencia de rebabas' WHERE ID = 3048;
-- UPDATE papoitem SET Description = N'aArea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 3001;
-- UPDATE papoitem SET Description = N'Estibador manual en buen estado.' WHERE ID = 3005;
-- UPDATE papoitem SET Description = N'No hay fugas ni goteos en las maquinas' WHERE ID = 3009;
-- UPDATE papoitem SET Description = N'Todas las resistencias se encuentras en buen estado.' WHERE ID = 3011;
-- UPDATE papoitem SET Description = N'Manometros calibrados y en buen estado.' WHERE ID = 3016;
-- UPDATE papoitem SET Description = N'Se encuentran las galgas en el puesto y con calibracion vigente.' WHERE ID = 3012;
-- UPDATE papoitem SET Description = N'Presion de aire alcanza el valor indicado en la prueba.' WHERE ID = 3017;
-- UPDATE papoitem SET Description = N'Los amperimetros estan funcionando.' WHERE ID = 3013;
-- UPDATE papoitem SET Description = N'El equipo opera correctamente.' WHERE ID = 3018;
-- UPDATE papoitem SET Description = N'Inexistencia de ruidos inusuales.' WHERE ID = 3014;
-- UPDATE papoitem SET Description = N'Inexistencia de ruidos inusuales.' WHERE ID = 3019;
-- UPDATE papoitem SET Description = N'Los instrumentos de medicion se encuentran calibrados.' WHERE ID = 3015;
-- TEXTO DE LA BASE 278: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 279: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 313: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 316: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 350: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3006: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3058: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3110: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3120: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3121: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3125: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 3138: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 7903: se queda el de papoitem (preguntas_texto_base.json)
