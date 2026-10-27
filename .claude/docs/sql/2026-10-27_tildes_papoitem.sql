-- Tildes y símbolos mal codificados en papoitem.Description (y registertype 13)
-- 2026-10-27 · texto UTF-8 leído como Latin-1 en la carga de la base: 'Ã³' por 'ó', 'aÂ\x93' por 'Ó' (la Ã perdió
-- la tilde), 'Â\x80Â\x93' por '–', 'Â±' por '±'. Cada UPDATE solo cambia el texto si sigue siendo el roto
-- (idempotente; sirve en cla-db-papo y en producción). No agrega tildes a palabras escritas sin ellas.
-- 62 ítems de papoitem + 1 de registertype.

SET XACT_ABORT ON;
BEGIN TRANSACTION;

-- 3030 EA11-4200 · PRESIÓN DE AIRE 6,2 bar +/- 0,2 bar
UPDATE papoitem SET Description = N'PRESIÓN DE AIRE 6,2 bar +/- 0,2 bar' WHERE ID = 3030 AND Description = N'PRESIaÂ' + NCHAR(147) + N'N DE AIRE 6,2 bar +/- 0,2 bar';
-- 3032 EA11-4200 · CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTEN
UPDATE papoitem SET Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_IZQ' WHERE ID = 3032 AND Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIaÂ' + NCHAR(147) + N'N PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_IZQ';
-- 3033 EA11-4200 · CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTEN
UPDATE papoitem SET Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_DER' WHERE ID = 3033 AND Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIaÂ' + NCHAR(147) + N'N PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_DER';
-- 4313 RE11-0101 · La presion de aire es la correcta para la operacion de la maquina (80–100 psi)
UPDATE papoitem SET Description = N'La presion de aire es la correcta para la operacion de la maquina (80–100 psi)' WHERE ID = 4313 AND Description = N'La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)';
-- 4314 RE11-0101 · Accion correctiva La presion de aire es la correcta para la operacion de la maquina (80–100 psi)
UPDATE papoitem SET Description = N'Accion correctiva La presion de aire es la correcta para la operacion de la maquina (80–100 psi)' WHERE ID = 4314 AND Description = N'Accion correctiva La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)';
-- 4315 RE11-0101 · Observacion La presion de aire es la correcta para la operacion de la maquina (80–100 psi)
UPDATE papoitem SET Description = N'Observacion La presion de aire es la correcta para la operacion de la maquina (80–100 psi)' WHERE ID = 4315 AND Description = N'Observacion La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)';
-- 4459 SO02-1006 · Extintor (si esta vencido, notificar a SST y cambiar) – incluye estado de la base porta extintor
UPDATE papoitem SET Description = N'Extintor (si esta vencido, notificar a SST y cambiar) – incluye estado de la base porta extintor' WHERE ID = 4459 AND Description = N'Extintor (si esta vencido, notificar a SST y cambiar) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' incluye estado de la base porta extintor';
-- 4485 SO02-1006 · Pinzas (horquillas) – si presenta anomalias, paro y notificar a mtto
UPDATE papoitem SET Description = N'Pinzas (horquillas) – si presenta anomalias, paro y notificar a mtto' WHERE ID = 4485 AND Description = N'Pinzas (horquillas) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto';
-- 4487 SO02-1006 · Funcionalidad cadenas y sistema hidraulico de levante y mangueras – si presenta anomalias, paro y notificar a 
UPDATE papoitem SET Description = N'Funcionalidad cadenas y sistema hidraulico de levante y mangueras – si presenta anomalias, paro y notificar a mtto' WHERE ID = 4487 AND Description = N'Funcionalidad cadenas y sistema hidraulico de levante y mangueras Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto';
-- 4489 SO02-1006 · Fugas (agua, aceites, combustible GLP, electrolito) – si presenta anomalias, paro y notificar a mtto
UPDATE papoitem SET Description = N'Fugas (agua, aceites, combustible GLP, electrolito) – si presenta anomalias, paro y notificar a mtto' WHERE ID = 4489 AND Description = N'Fugas (agua, aceites, combustible GLP, electrolito) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto';
-- 4491 SO02-1006 · Sensor de velocidad – si presenta anomalias, paro y notificar a mtto
UPDATE papoitem SET Description = N'Sensor de velocidad – si presenta anomalias, paro y notificar a mtto' WHERE ID = 4491 AND Description = N'Sensor de velocidad Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto';
-- 4500 SO02-4502 · Hallazgo La botonera funciona correctamente de acuerdo a la senalizacion ↑→↓← y parada de emergencia
UPDATE papoitem SET Description = N'Hallazgo La botonera funciona correctamente de acuerdo a la senalizacion ↑→↓← y parada de emergencia' WHERE ID = 4500 AND Description = N'Hallazgo La botonera funciona correctamente de acuerdo a la senalizacion Â' + NCHAR(134) + N'Â' + NCHAR(145) + N'Â' + NCHAR(134) + N'Â' + NCHAR(146) + N'Â' + NCHAR(134) + N'Â' + NCHAR(147) + N'Â' + NCHAR(134) + N'Â' + NCHAR(144) + N' y parada de emergencia';
-- 5109 EC11-0101 · Guardas de seguridad bien colocadas. Área libre de objetos extranos que puedan causar perdida de equilibrio.
UPDATE papoitem SET Description = N'Guardas de seguridad bien colocadas. Área libre de objetos extranos que puedan causar perdida de equilibrio.' WHERE ID = 5109 AND Description = N'Guardas de seguridad bien colocadas. aÂ' + NCHAR(129) + N'rea libre de objetos extranos que puedan causar perdida de equilibrio.';
-- 5111 EC11-0101 · Se encuentra habilitado y en buen estado la Celda Robotica, las Barreras Ópticas y Sistemas de Seguridad de pa
UPDATE papoitem SET Description = N'Se encuentra habilitado y en buen estado la Celda Robotica, las Barreras Ópticas y Sistemas de Seguridad de parada de Emergencia del Robot.' WHERE ID = 5111 AND Description = N'Se encuentra habilitado y en buen estado la Celda Robotica, las Barreras aÂ' + NCHAR(147) + N'pticas y Sistemas de Seguridad de parada de Emergencia del Robot.';
-- 5214 MZ07-0101 · Óxido de plomo (kg)
UPDATE papoitem SET Description = N'Óxido de plomo (kg)' WHERE ID = 5214 AND Description = N'aÂ' + NCHAR(147) + N'xido de plomo (kg)';
-- 5573 AC10-1003 · LLeva cubrebornes y están bien puestos.
UPDATE papoitem SET Description = N'LLeva cubrebornes y están bien puestos.' WHERE ID = 5573 AND Description = N'LLeva cubrebornes y estaÂ n bien puestos.';
-- 5578 AC10-0801 · Cumple con el estandar de limpieza del puesto de trabajo / manual de referencia para aplicacion de 5´s
UPDATE papoitem SET Description = N'Cumple con el estandar de limpieza del puesto de trabajo / manual de referencia para aplicacion de 5´s' WHERE ID = 5578 AND Description = N'Cumple con el estandar de limpieza del puesto de trabajo / manual de referencia para aplicacion de 5Â´s';
-- 5605 AC10-0801 · Último numero de garantia del turno
UPDATE papoitem SET Description = N'Último numero de garantia del turno' WHERE ID = 5605 AND Description = N'aÂ' + NCHAR(154) + N'ltimo numero de garantia del turno';
-- 6214 TE11-2601 · Área de trabajo aseada y libre de obstaculos cumpliendo estandar 5S
UPDATE papoitem SET Description = N'Área de trabajo aseada y libre de obstaculos cumpliendo estandar 5S' WHERE ID = 6214 AND Description = N'aÂ' + NCHAR(129) + N'rea de trabajo aseada y libre de obstaculos cumpliendo estandar 5S';
-- 9171 PL11-0101-CA · Área limpia y en orden (libre de objetos extranos, piso libre de aceite y agua).
UPDATE papoitem SET Description = N'Área limpia y en orden (libre de objetos extranos, piso libre de aceite y agua).' WHERE ID = 9171 AND Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden (libre de objetos extranos, piso libre de aceite y agua).';
-- 10379 PL11-0101-CU · Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)
UPDATE papoitem SET Description = N'Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)' WHERE ID = 10379 AND Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)';
-- 10389 PL11-0101-CU · CAV1(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga ce
UPDATE papoitem SET Description = N'CAV1(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10389 AND Description = N'CAV1(primera)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- 10390 PL11-0101-CU · CAV1(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga cen
UPDATE papoitem SET Description = N'CAV1(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10390 AND Description = N'CAV1(ultima)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- 10391 PL11-0101-CU · CAV2(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga ce
UPDATE papoitem SET Description = N'CAV2(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10391 AND Description = N'CAV2(primera)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- 10392 PL11-0101-CU · CAV2(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga cen
UPDATE papoitem SET Description = N'CAV2(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10392 AND Description = N'CAV2(ultima)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- 10782 PL11-0101-S&A · Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)
UPDATE papoitem SET Description = N'Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)' WHERE ID = 10782 AND Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)';
-- 11176 EA11-1601 · Cabinas eléctricas cerradas
UPDATE papoitem SET Description = N'Cabinas eléctricas cerradas' WHERE ID = 11176 AND Description = N'Cabinas elÃ©ctricas cerradas';
-- 11177 EA11-1601 · Cabinas eléctricas con libre acceso
UPDATE papoitem SET Description = N'Cabinas eléctricas con libre acceso' WHERE ID = 11177 AND Description = N'Cabinas elÃ©ctricas con libre acceso';
-- 11178 EA11-1601 · No hay objetos dentro ni sobre las cabinas eléctricas
UPDATE papoitem SET Description = N'No hay objetos dentro ni sobre las cabinas eléctricas' WHERE ID = 11178 AND Description = N'No hay objetos dentro ni sobre las cabinas elÃ©ctricas';
-- 11181 EA11-1601 · No hay fugas de aire y/o aceite ni goteos en las máquinas
UPDATE papoitem SET Description = N'No hay fugas de aire y/o aceite ni goteos en las máquinas' WHERE ID = 11181 AND Description = N'No hay fugas de aire y/o aceite ni goteos en las mÃ¡quinas';
-- 11182 EA11-1601 · Area de trabajo aseada y libre de obstáculos cumpliendo estándar 5'S
UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstáculos cumpliendo estándar 5''S' WHERE ID = 11182 AND Description = N'Area de trabajo aseada y libre de obstÃ¡culos cumpliendo estÃ¡ndar 5''S';
-- 11185 EA11-1601 · Máquina se encuentra lubricada
UPDATE papoitem SET Description = N'Máquina se encuentra lubricada' WHERE ID = 11185 AND Description = N'MÃ¡quina se encuentra lubricada';
-- 11187 EA11-1601 · Controles están dando salida de voltaje a través de los amperímetros
UPDATE papoitem SET Description = N'Controles están dando salida de voltaje a través de los amperímetros' WHERE ID = 11187 AND Description = N'Controles estÃ¡n dando salida de voltaje a travÃ©s de los amperÃ­metros';
-- 11188 EA11-1601 · Enciende la pantalla del PLC al prender la máquina
UPDATE papoitem SET Description = N'Enciende la pantalla del PLC al prender la máquina' WHERE ID = 11188 AND Description = N'Enciende la pantalla del PLC al prender la mÃ¡quina';
-- 11190 EA11-1601 · El Nivel de aceite es adecuado en la unidad de mantenimiento neumático
UPDATE papoitem SET Description = N'El Nivel de aceite es adecuado en la unidad de mantenimiento neumático' WHERE ID = 11190 AND Description = N'El Nivel de aceite es adecuado en la unidad de mantenimiento neumÃ¡tico';
-- 11192 EA11-1601 · Galgas ubicadas cerca a la máquina
UPDATE papoitem SET Description = N'Galgas ubicadas cerca a la máquina' WHERE ID = 11192 AND Description = N'Galgas ubicadas cerca a la mÃ¡quina';
-- 11194 EA11-1601 · Las boquillas están limpias y en buen estado
UPDATE papoitem SET Description = N'Las boquillas están limpias y en buen estado' WHERE ID = 11194 AND Description = N'Las boquillas estÃ¡n limpias y en buen estado';
-- 11195 EA11-1601 · Presión de aire (SetPoint: 100, Variación: ±20 psi)
UPDATE papoitem SET Description = N'Presión de aire (SetPoint: 100, Variación: ±20 psi)' WHERE ID = 11195 AND Description = N'PresiÃ³n de aire (SetPoint: 100, VariaciÃ³n: Â±20 psi)';
-- 11196 EA11-1601 · Temperatura 1 Izquierda (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11196 AND Description = N'Temperatura 1 Izquierda (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11197 EA11-1601 · Temperatura 2 Derecha (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 2 Derecha (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11197 AND Description = N'Temperatura 2 Derecha (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11198 EA11-1601 · Temperatura 1 Izquierda (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11198 AND Description = N'Temperatura 1 Izquierda (BaterÃ­a PequeÃ±a - Conjunto color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11199 EA11-1601 · Temperatura 2 Derecha (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 2 Derecha (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11199 AND Description = N'Temperatura 2 Derecha (BaterÃ­a PequeÃ±a - Conjunto color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11200 EA11-1601 · Temperatura 1 Izquierda (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11200 AND Description = N'Temperatura 1 Izquierda (BaterÃ­a PequeÃ±a - Negro - Color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11201 EA11-1601 · Temperatura 2 Derecha (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)
UPDATE papoitem SET Description = N'Temperatura 2 Derecha (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)' WHERE ID = 11201 AND Description = N'Temperatura 2 Derecha (BaterÃ­a PequeÃ±a - Negro - Color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)';
-- 11202 EA11-1601 · Tiempo de Queme (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0.5/+1 seg)
UPDATE papoitem SET Description = N'Tiempo de Queme (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0.5/+1 seg)' WHERE ID = 11202 AND Description = N'Tiempo de Queme (Sg) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 4.0 seg, VariaciÃ³n: -0.5/+1 seg)';
-- 11204 EA11-1601 · Tiempo de sellado o Reposo (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0/+2 seg)
UPDATE papoitem SET Description = N'Tiempo de sellado o Reposo (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0/+2 seg)' WHERE ID = 11204 AND Description = N'Tiempo de sellado o Reposo (Sg) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 4.0 seg, VariaciÃ³n: -0/+2 seg)';
-- 11206 EA11-1601 · Corriente Amperimetros Termoselladora. Valores por debajo es obligacion corregir con el electrico (Amp) - (Bat
UPDATE papoitem SET Description = N'Corriente Amperimetros Termoselladora. Valores por debajo es obligacion corregir con el electrico (Amp) - (Batería Grande - Batería Pequeña) (Rango requerido: 17-20 Amp)' WHERE ID = 11206 AND Description = N'Corriente Amperimetros Termoselladora. Valores por debajo es obligacion corregir con el electrico (Amp) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (Rango requerido: 17-20 Amp)';
-- 11211 EA11-1601 · El tiempo de presurización U1 (Valor requerido: 3 Segundos)
UPDATE papoitem SET Description = N'El tiempo de presurización U1 (Valor requerido: 3 Segundos)' WHERE ID = 11211 AND Description = N'El tiempo de presurizaciÃ³n U1 (Valor requerido: 3 Segundos)';
-- 11212 EA11-1601 · El tiempo de presurización Bat. Restantes (Valor requerido: 5 Segundos)
UPDATE papoitem SET Description = N'El tiempo de presurización Bat. Restantes (Valor requerido: 5 Segundos)' WHERE ID = 11212 AND Description = N'El tiempo de presurizaciÃ³n Bat. Restantes (Valor requerido: 5 Segundos)';
-- 11213 EA11-1601 · El tiempo de prueba Todas las Baterías (Valor requerido: 4 Segundos)
UPDATE papoitem SET Description = N'El tiempo de prueba Todas las Baterías (Valor requerido: 4 Segundos)' WHERE ID = 11213 AND Description = N'El tiempo de prueba Todas las BaterÃ­as (Valor requerido: 4 Segundos)';
-- 11214 EA11-1601 · Presión cilindro vertical probadora de Fugas (Valor requerido: 80 PSI)
UPDATE papoitem SET Description = N'Presión cilindro vertical probadora de Fugas (Valor requerido: 80 PSI)' WHERE ID = 11214 AND Description = N'PresiÃ³n cilindro vertical probadora de Fugas (Valor requerido: 80 PSI)';
-- 11215 EA11-1601 · Verificacion de DAPE con muestra patrón. Control Hora a Hora. En caso de No rechazar la Muestra Patron. Parar 
UPDATE papoitem SET Description = N'Verificacion de DAPE con muestra patrón. Control Hora a Hora. En caso de No rechazar la Muestra Patron. Parar Proceso e Informar a Supervisor de Produccion y Mantenimiento' WHERE ID = 11215 AND Description = N'Verificacion de DAPE con muestra patrÃ³n. Control Hora a Hora. En caso de No rechazar la Muestra Patron. Parar Proceso e Informar a Supervisor de Produccion y Mantenimiento';
-- 11216 EA11-1601 · Tipo de caja y cubierta según referencia de bateria
UPDATE papoitem SET Description = N'Tipo de caja y cubierta según referencia de bateria' WHERE ID = 11216 AND Description = N'Tipo de caja y cubierta segÃºn referencia de bateria';
-- 11217 EA11-1601 · Polaridad Correcta según Programa de Producción
UPDATE papoitem SET Description = N'Polaridad Correcta según Programa de Producción' WHERE ID = 11217 AND Description = N'Polaridad Correcta segÃºn Programa de ProducciÃ³n';
-- 11218 EA11-1601 · Cubiertas sin Rechupes y/o contracción
UPDATE papoitem SET Description = N'Cubiertas sin Rechupes y/o contracción' WHERE ID = 11218 AND Description = N'Cubiertas sin Rechupes y/o contracciÃ³n';
-- 11219 EA11-1601 · Prueba de queme caja y cubierta (verificación labios de queme parejos)
UPDATE papoitem SET Description = N'Prueba de queme caja y cubierta (verificación labios de queme parejos)' WHERE ID = 11219 AND Description = N'Prueba de queme caja y cubierta (verificaciÃ³n labios de queme parejos)';
-- 11222 EA11-1601 · Planitud cubierta después de Termosellado baterías selladas
UPDATE papoitem SET Description = N'Planitud cubierta después de Termosellado baterías selladas' WHERE ID = 11222 AND Description = N'Planitud cubierta despuÃ©s de Termosellado baterÃ­as selladas';
-- 11225 EA11-1601 · Probador de Fuga automatico verificacion de DAPE con muestra patrón
UPDATE papoitem SET Description = N'Probador de Fuga automatico verificacion de DAPE con muestra patrón' WHERE ID = 11225 AND Description = N'Probador de Fuga automatico verificacion de DAPE con muestra patrÃ³n';
-- 11227 EA11-1601 · Estan las borneras según ref. a fabricar
UPDATE papoitem SET Description = N'Estan las borneras según ref. a fabricar' WHERE ID = 11227 AND Description = N'Estan las borneras segÃºn ref. a fabricar';
-- 11232 EA11-1601 · Fusión espigo vs buje (cada inicio de turno o cambio de referencia)
UPDATE papoitem SET Description = N'Fusión espigo vs buje (cada inicio de turno o cambio de referencia)' WHERE ID = 11232 AND Description = N'FusiÃ³n espigo vs buje (cada inicio de turno o cambio de referencia)';
-- 'A' + byte suelto (la Ã perdió la tilde y el segundo byte quedó como carácter de control): A\x81 -> Á
-- 133 · Área de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cab
UPDATE papoitem SET Description = N'Área de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 133 AND Description = N'A' + NCHAR(129) + N'rea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.';
-- 6803 · Ángulo de volcado vs especificacion
UPDATE papoitem SET Description = N'Ángulo de volcado vs especificacion' WHERE ID = 6803 AND Description = N'A' + NCHAR(129) + N'ngulo de volcado vs especificacion';

-- registertype 13 (texto con bytes perdidos, corrección manual)
UPDATE registertype SET Description = N'Al inicio, cada cambio de referencia, después de un mantenimiento y cada 30 minutos' WHERE ID = 13 AND Description = N'Al inicio, cada cambio de referencia, despuÃ???Ã??Ã?Â©s de un mantenimiento y cada 30 minutos';

COMMIT;

-- Rollback (vuelve al texto roto):
-- UPDATE papoitem SET Description = N'PRESIaÂ' + NCHAR(147) + N'N DE AIRE 6,2 bar +/- 0,2 bar' WHERE ID = 3030 AND Description = N'PRESIÓN DE AIRE 6,2 bar +/- 0,2 bar';
-- UPDATE papoitem SET Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIaÂ' + NCHAR(147) + N'N PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_IZQ' WHERE ID = 3032 AND Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_IZQ';
-- UPDATE papoitem SET Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIaÂ' + NCHAR(147) + N'N PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_DER' WHERE ID = 3033 AND Description = N'CORRIENTE AMPERIMETROS 19 Amp +1/-2 Amp (VALORES POR DEBAJO ES OBLIGACIÓN PARAR PROCESO Y CAMBIAR LAS RESISTENCIAS MALAS)_DER';
-- UPDATE papoitem SET Description = N'La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)' WHERE ID = 4313 AND Description = N'La presion de aire es la correcta para la operacion de la maquina (80–100 psi)';
-- UPDATE papoitem SET Description = N'Accion correctiva La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)' WHERE ID = 4314 AND Description = N'Accion correctiva La presion de aire es la correcta para la operacion de la maquina (80–100 psi)';
-- UPDATE papoitem SET Description = N'Observacion La presion de aire es la correcta para la operacion de la maquina (80Â' + NCHAR(128) + N'Â' + NCHAR(147) + N'100 psi)' WHERE ID = 4315 AND Description = N'Observacion La presion de aire es la correcta para la operacion de la maquina (80–100 psi)';
-- UPDATE papoitem SET Description = N'Extintor (si esta vencido, notificar a SST y cambiar) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' incluye estado de la base porta extintor' WHERE ID = 4459 AND Description = N'Extintor (si esta vencido, notificar a SST y cambiar) – incluye estado de la base porta extintor';
-- UPDATE papoitem SET Description = N'Pinzas (horquillas) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto' WHERE ID = 4485 AND Description = N'Pinzas (horquillas) – si presenta anomalias, paro y notificar a mtto';
-- UPDATE papoitem SET Description = N'Funcionalidad cadenas y sistema hidraulico de levante y mangueras Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto' WHERE ID = 4487 AND Description = N'Funcionalidad cadenas y sistema hidraulico de levante y mangueras – si presenta anomalias, paro y notificar a mtto';
-- UPDATE papoitem SET Description = N'Fugas (agua, aceites, combustible GLP, electrolito) Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto' WHERE ID = 4489 AND Description = N'Fugas (agua, aceites, combustible GLP, electrolito) – si presenta anomalias, paro y notificar a mtto';
-- UPDATE papoitem SET Description = N'Sensor de velocidad Â' + NCHAR(128) + N'Â' + NCHAR(147) + N' si presenta anomalias, paro y notificar a mtto' WHERE ID = 4491 AND Description = N'Sensor de velocidad – si presenta anomalias, paro y notificar a mtto';
-- UPDATE papoitem SET Description = N'Hallazgo La botonera funciona correctamente de acuerdo a la senalizacion Â' + NCHAR(134) + N'Â' + NCHAR(145) + N'Â' + NCHAR(134) + N'Â' + NCHAR(146) + N'Â' + NCHAR(134) + N'Â' + NCHAR(147) + N'Â' + NCHAR(134) + N'Â' + NCHAR(144) + N' y parada de emergencia' WHERE ID = 4500 AND Description = N'Hallazgo La botonera funciona correctamente de acuerdo a la senalizacion ↑→↓← y parada de emergencia';
-- UPDATE papoitem SET Description = N'Guardas de seguridad bien colocadas. aÂ' + NCHAR(129) + N'rea libre de objetos extranos que puedan causar perdida de equilibrio.' WHERE ID = 5109 AND Description = N'Guardas de seguridad bien colocadas. Área libre de objetos extranos que puedan causar perdida de equilibrio.';
-- UPDATE papoitem SET Description = N'Se encuentra habilitado y en buen estado la Celda Robotica, las Barreras aÂ' + NCHAR(147) + N'pticas y Sistemas de Seguridad de parada de Emergencia del Robot.' WHERE ID = 5111 AND Description = N'Se encuentra habilitado y en buen estado la Celda Robotica, las Barreras Ópticas y Sistemas de Seguridad de parada de Emergencia del Robot.';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(147) + N'xido de plomo (kg)' WHERE ID = 5214 AND Description = N'Óxido de plomo (kg)';
-- UPDATE papoitem SET Description = N'LLeva cubrebornes y estaÂ n bien puestos.' WHERE ID = 5573 AND Description = N'LLeva cubrebornes y están bien puestos.';
-- UPDATE papoitem SET Description = N'Cumple con el estandar de limpieza del puesto de trabajo / manual de referencia para aplicacion de 5Â´s' WHERE ID = 5578 AND Description = N'Cumple con el estandar de limpieza del puesto de trabajo / manual de referencia para aplicacion de 5´s';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(154) + N'ltimo numero de garantia del turno' WHERE ID = 5605 AND Description = N'Último numero de garantia del turno';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(129) + N'rea de trabajo aseada y libre de obstaculos cumpliendo estandar 5S' WHERE ID = 6214 AND Description = N'Área de trabajo aseada y libre de obstaculos cumpliendo estandar 5S';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden (libre de objetos extranos, piso libre de aceite y agua).' WHERE ID = 9171 AND Description = N'Área limpia y en orden (libre de objetos extranos, piso libre de aceite y agua).';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)' WHERE ID = 10379 AND Description = N'Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)';
-- UPDATE papoitem SET Description = N'CAV1(primera)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10389 AND Description = N'CAV1(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- UPDATE papoitem SET Description = N'CAV1(ultima)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10390 AND Description = N'CAV1(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- UPDATE papoitem SET Description = N'CAV2(primera)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10391 AND Description = N'CAV2(primera)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- UPDATE papoitem SET Description = N'CAV2(ultima)//Cubierta con bujes no deformados (aÂ' + NCHAR(152) + N' interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)' WHERE ID = 10392 AND Description = N'CAV2(ultima)//Cubierta con bujes no deformados (Ø interno de buje, altura de buje y galga de espigo. Galga centrado de buje aplica solo cubierta 42)';
-- UPDATE papoitem SET Description = N'aÂ' + NCHAR(129) + N'rea limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)' WHERE ID = 10782 AND Description = N'Área limpia y en orden. (Libre de objetos extranos, piso libre de aceite y agua)';
-- UPDATE papoitem SET Description = N'Cabinas elÃ©ctricas cerradas' WHERE ID = 11176 AND Description = N'Cabinas eléctricas cerradas';
-- UPDATE papoitem SET Description = N'Cabinas elÃ©ctricas con libre acceso' WHERE ID = 11177 AND Description = N'Cabinas eléctricas con libre acceso';
-- UPDATE papoitem SET Description = N'No hay objetos dentro ni sobre las cabinas elÃ©ctricas' WHERE ID = 11178 AND Description = N'No hay objetos dentro ni sobre las cabinas eléctricas';
-- UPDATE papoitem SET Description = N'No hay fugas de aire y/o aceite ni goteos en las mÃ¡quinas' WHERE ID = 11181 AND Description = N'No hay fugas de aire y/o aceite ni goteos en las máquinas';
-- UPDATE papoitem SET Description = N'Area de trabajo aseada y libre de obstÃ¡culos cumpliendo estÃ¡ndar 5''S' WHERE ID = 11182 AND Description = N'Area de trabajo aseada y libre de obstáculos cumpliendo estándar 5''S';
-- UPDATE papoitem SET Description = N'MÃ¡quina se encuentra lubricada' WHERE ID = 11185 AND Description = N'Máquina se encuentra lubricada';
-- UPDATE papoitem SET Description = N'Controles estÃ¡n dando salida de voltaje a travÃ©s de los amperÃ­metros' WHERE ID = 11187 AND Description = N'Controles están dando salida de voltaje a través de los amperímetros';
-- UPDATE papoitem SET Description = N'Enciende la pantalla del PLC al prender la mÃ¡quina' WHERE ID = 11188 AND Description = N'Enciende la pantalla del PLC al prender la máquina';
-- UPDATE papoitem SET Description = N'El Nivel de aceite es adecuado en la unidad de mantenimiento neumÃ¡tico' WHERE ID = 11190 AND Description = N'El Nivel de aceite es adecuado en la unidad de mantenimiento neumático';
-- UPDATE papoitem SET Description = N'Galgas ubicadas cerca a la mÃ¡quina' WHERE ID = 11192 AND Description = N'Galgas ubicadas cerca a la máquina';
-- UPDATE papoitem SET Description = N'Las boquillas estÃ¡n limpias y en buen estado' WHERE ID = 11194 AND Description = N'Las boquillas están limpias y en buen estado';
-- UPDATE papoitem SET Description = N'PresiÃ³n de aire (SetPoint: 100, VariaciÃ³n: Â±20 psi)' WHERE ID = 11195 AND Description = N'Presión de aire (SetPoint: 100, Variación: ±20 psi)';
-- UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11196 AND Description = N'Temperatura 1 Izquierda (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Temperatura 2 Derecha (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11197 AND Description = N'Temperatura 2 Derecha (Batería Grande - Batería Pequeña) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (BaterÃ­a PequeÃ±a - Conjunto color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11198 AND Description = N'Temperatura 1 Izquierda (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Temperatura 2 Derecha (BaterÃ­a PequeÃ±a - Conjunto color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11199 AND Description = N'Temperatura 2 Derecha (Batería Pequeña - Conjunto color) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Temperatura 1 Izquierda (BaterÃ­a PequeÃ±a - Negro - Color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11200 AND Description = N'Temperatura 1 Izquierda (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Temperatura 2 Derecha (BaterÃ­a PequeÃ±a - Negro - Color) (SetPoint: 300, VariaciÃ³n: Â±20Â°C)' WHERE ID = 11201 AND Description = N'Temperatura 2 Derecha (Batería Pequeña - Negro - Color) (SetPoint: 300, Variación: ±20°C)';
-- UPDATE papoitem SET Description = N'Tiempo de Queme (Sg) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 4.0 seg, VariaciÃ³n: -0.5/+1 seg)' WHERE ID = 11202 AND Description = N'Tiempo de Queme (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0.5/+1 seg)';
-- UPDATE papoitem SET Description = N'Tiempo de sellado o Reposo (Sg) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (SetPoint: 4.0 seg, VariaciÃ³n: -0/+2 seg)' WHERE ID = 11204 AND Description = N'Tiempo de sellado o Reposo (Sg) - (Batería Grande - Batería Pequeña) (SetPoint: 4.0 seg, Variación: -0/+2 seg)';
-- UPDATE papoitem SET Description = N'Corriente Amperimetros Termoselladora. Valores por debajo es obligacion corregir con el electrico (Amp) - (BaterÃ­a Grande - BaterÃ­a PequeÃ±a) (Rango requerido: 17-20 Amp)' WHERE ID = 11206 AND Description = N'Corriente Amperimetros Termoselladora. Valores por debajo es obligacion corregir con el electrico (Amp) - (Batería Grande - Batería Pequeña) (Rango requerido: 17-20 Amp)';
-- UPDATE papoitem SET Description = N'El tiempo de presurizaciÃ³n U1 (Valor requerido: 3 Segundos)' WHERE ID = 11211 AND Description = N'El tiempo de presurización U1 (Valor requerido: 3 Segundos)';
-- UPDATE papoitem SET Description = N'El tiempo de presurizaciÃ³n Bat. Restantes (Valor requerido: 5 Segundos)' WHERE ID = 11212 AND Description = N'El tiempo de presurización Bat. Restantes (Valor requerido: 5 Segundos)';
-- UPDATE papoitem SET Description = N'El tiempo de prueba Todas las BaterÃ­as (Valor requerido: 4 Segundos)' WHERE ID = 11213 AND Description = N'El tiempo de prueba Todas las Baterías (Valor requerido: 4 Segundos)';
-- UPDATE papoitem SET Description = N'PresiÃ³n cilindro vertical probadora de Fugas (Valor requerido: 80 PSI)' WHERE ID = 11214 AND Description = N'Presión cilindro vertical probadora de Fugas (Valor requerido: 80 PSI)';
-- UPDATE papoitem SET Description = N'Verificacion de DAPE con muestra patrÃ³n. Control Hora a Hora. En caso de No rechazar la Muestra Patron. Parar Proceso e Informar a Supervisor de Produccion y Mantenimiento' WHERE ID = 11215 AND Description = N'Verificacion de DAPE con muestra patrón. Control Hora a Hora. En caso de No rechazar la Muestra Patron. Parar Proceso e Informar a Supervisor de Produccion y Mantenimiento';
-- UPDATE papoitem SET Description = N'Tipo de caja y cubierta segÃºn referencia de bateria' WHERE ID = 11216 AND Description = N'Tipo de caja y cubierta según referencia de bateria';
-- UPDATE papoitem SET Description = N'Polaridad Correcta segÃºn Programa de ProducciÃ³n' WHERE ID = 11217 AND Description = N'Polaridad Correcta según Programa de Producción';
-- UPDATE papoitem SET Description = N'Cubiertas sin Rechupes y/o contracciÃ³n' WHERE ID = 11218 AND Description = N'Cubiertas sin Rechupes y/o contracción';
-- UPDATE papoitem SET Description = N'Prueba de queme caja y cubierta (verificaciÃ³n labios de queme parejos)' WHERE ID = 11219 AND Description = N'Prueba de queme caja y cubierta (verificación labios de queme parejos)';
-- UPDATE papoitem SET Description = N'Planitud cubierta despuÃ©s de Termosellado baterÃ­as selladas' WHERE ID = 11222 AND Description = N'Planitud cubierta después de Termosellado baterías selladas';
-- UPDATE papoitem SET Description = N'Probador de Fuga automatico verificacion de DAPE con muestra patrÃ³n' WHERE ID = 11225 AND Description = N'Probador de Fuga automatico verificacion de DAPE con muestra patrón';
-- UPDATE papoitem SET Description = N'Estan las borneras segÃºn ref. a fabricar' WHERE ID = 11227 AND Description = N'Estan las borneras según ref. a fabricar';
-- UPDATE papoitem SET Description = N'FusiÃ³n espigo vs buje (cada inicio de turno o cambio de referencia)' WHERE ID = 11232 AND Description = N'Fusión espigo vs buje (cada inicio de turno o cambio de referencia)';
-- UPDATE papoitem SET Description = N'A' + NCHAR(129) + N'rea de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.' WHERE ID = 133 AND Description = N'Área de trabajo aseada y libre de obstaculos cumpliendo el estandar 5S. No hay objetos dentro ni sobre las cabinas electricas.';
-- UPDATE papoitem SET Description = N'A' + NCHAR(129) + N'ngulo de volcado vs especificacion' WHERE ID = 6803 AND Description = N'Ángulo de volcado vs especificacion';
-- UPDATE registertype SET Description = N'Al inicio, cada cambio de referencia, despuÃ???Ã??Ã?Â©s de un mantenimiento y cada 30 minutos' WHERE ID = 13 AND Description = N'Al inicio, cada cambio de referencia, después de un mantenimiento y cada 30 minutos';
