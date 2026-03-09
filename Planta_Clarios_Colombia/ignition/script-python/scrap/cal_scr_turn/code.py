# Project Library → Scrap → cal_scr_turn
def calcularScrapTurnos(
    tag_negativo="[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/Edge/Tag Plc/Peso Scrap Negativo",
    tag_positivo="[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/Edge/Tag Plc/Peso Scrap Positivo"
):

    import system
    import datetime

    # ---------------------------
    # Turnos
    # ---------------------------
    TURNOS = {
        "T1": (22, 6),   # 22:00 a 06:00
        "T2": (6, 14),   # 06:00 a 14:00
        "T3": (14, 22)   # 14:00 a 22:00
    }

    ahora = datetime.datetime.now()
    hora = ahora.hour

    # ---------------------------
    # Determinar turno actual
    # ---------------------------
    turno_actual = None
    for t, (ini, fin) in TURNOS.items():
        if ini < fin:
            if ini <= hora < fin:
                turno_actual = t
        else:
            if hora >= ini or hora < fin:
                turno_actual = t

    # ---------------------------
    # Rango de turno
    # ---------------------------
    if turno_actual == "T1":
        if hora >= 22:
            inicio_turno = ahora.replace(hour=22, minute=0, second=0, microsecond=0)
            fin_turno = (ahora + datetime.timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        else:
            inicio_turno = (ahora - datetime.timedelta(days=1)).replace(hour=22, minute=0, second=0, microsecond=0)
            fin_turno = ahora.replace(hour=6, minute=0, second=0, microsecond=0)
    else:
        ini, fin = TURNOS[turno_actual]
        inicio_turno = ahora.replace(hour=ini, minute=0, second=0, microsecond=0)
        fin_turno = ahora.replace(hour=fin, minute=0, second=0, microsecond=0)

    # ---------------------------
    # Día productivo (empieza 22:00)
    # ---------------------------
    if hora < 22:
        inicio_dia = (ahora - datetime.timedelta(days=1)).replace(hour=22, minute=0, second=0, microsecond=0)
    else:
        inicio_dia = ahora.replace(hour=22, minute=0, second=0, microsecond=0)

    fin_dia = ahora

    # ---------------------------
    # Función histórico
    # ---------------------------
    def leer_total(tag, inicio, fin):
        data = system.tag.queryTagHistory(
            paths=[tag],
            startDate=inicio,
            endDate=fin,
            aggregationMode="Average"
        )
    
        total = 0
    
        if data is None:
            return 0
    
        rows = data.getRowCount()
    
        for i in range(rows):
            val = data.getValueAt(i, 1)   # Columna 1 = valor
            if val is not None:
                total += float(val)
    
        return total

    # ---------------------------
    # Cálculos
    # ---------------------------
    total_neg = leer_total(tag_negativo, inicio_turno, fin_turno)
    total_pos = leer_total(tag_positivo, inicio_turno, fin_turno)

    dia_neg = leer_total(tag_negativo, inicio_dia, fin_dia)
    dia_pos = leer_total(tag_positivo, inicio_dia, fin_dia)

    neto = total_pos - total_neg

    # ---------------------------
    # Resultado
    # ---------------------------
    return {
        "TurnoActual": turno_actual,
        "TotalTurnoNeg": total_neg,
        "TotalTurnoPos": total_pos,
        "AcumuladoDiaNeg": dia_neg,
        "AcumuladoDiaPos": dia_pos,
        "NetoTurnoActual": neto,
        "InicioTurno": inicio_turno,
        "FinTurno": fin_turno,
        "InicioDia": inicio_dia,
        "FinDia": fin_dia
    }
def actualizarTagsPorTrigger():
   
    """
    Actualiza tags de scrap por turno y de turno actual.
    Lee los totales desde calcularScrapTurnos() y escribe en:
      - Scrap Neg Turno {1,2,3}
      - Scrap Pos Turno {1,2,3}
      - Scrap Neg Turno Actual
      - Scrap Pos Turno Actual
    """
    import system
    logger = system.util.getLogger("Scrap")

    try:
        # Import explícito del módulo para evitar confusiones de scope
        import Scrap.cal_scr_turn as cal
        res = cal.calcularScrapTurnos()
    except Exception as e:
        logger.error("Error llamando calcularScrapTurnos(): %s" % e)
        return

    if not isinstance(res, dict):
        logger.error("calcularScrapTurnos() no devolvió un dict. Valor devuelto: %r" % res)
        return

    # Validar turno
    turno_actual = res.get("TurnoActual", None)
    if turno_actual not in ("T1", "T2", "T3"):
        logger.error("TurnoActual inválido o None: %r. No se escribirán tags." % turno_actual)
        return

    # Mapas de tags por turno
    tags_neg = {
        "T1": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Neg Turno 1",
        "T2": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Neg Turno 2",
        "T3": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Neg Turno 3"
    }
    tags_pos = {
        "T1": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Pos Turno 1",
        "T2": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Pos Turno 2",
        "T3": "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Pos Turno 3"
    }

    # Tomar valores usando las CLAVES REALES del dict
    # (antes usabas ValorTurnoActualNeg/Pos → no existen)
    total_neg_turno = res.get("TotalTurnoNeg", 0.0)
    total_pos_turno = res.get("TotalTurnoPos", 0.0)

    # Escribir en los tags del turno correspondiente (línea 133 anterior)
    try:
        system.tag.writeBlocking(
            [tags_neg[turno_actual], tags_pos[turno_actual]],
            [total_neg_turno,        total_pos_turno]
        )
    except Exception as e:
        logger.error("Error escribiendo tags de turno %s: %s" % (turno_actual, e))

    # Escribir en los tags de Turno Actual
    try:
        system.tag.writeBlocking(
            [
                "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Neg Turno Actual",
                "[default]Clarios/Yumbo/Scrap/Ensamble/Linea 4/line/Scrap Turno/Scrap Pos Turno Actual"
            ],
            [total_neg_turno, total_pos_turno]
        )
    except Exception as e:
        logger.error("Error escribiendo tags de Turno Actual: %s" % e)

    # (Opcional) Log informativo
    logger.info("Turno %s actualizado. Neg=%.3f, Pos=%.3f" % (turno_actual, total_neg_turno, total_pos_turno))