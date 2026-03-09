# Script Library: paros_por_cambio_densidad
# Autor: César A. Muñoz + Copilot
# Objetivo: Tabla por fecha y por turno del tiempo detenido (sin producción) de cada cambio de densidad,
#           atribuyendo el paro íntegro al turno en que inicia el paro e incluyendo SP anterior.

# ===== Configuración con tus TAGS =====
TAG_SP = "[default]NFR/Acabado/LLenadora Final SLI/Densidad_Segundo_Llenado_SP"
TAG_ESTADO = "[default]NFR/Acabado/LLenadora Final SLI/Llenadora/Estatus"

# Estados
VAL_STOP = 2    # "sin producción"
VAL_RUN  = 6    # "productivo"

# Turnos (confirmados)
TURNOS = [
    {"name": "Turno 1", "startHour": 22},  # 22:00 (del día) -> 06:00 (día siguiente)
    {"name": "Turno 2", "startHour": 6},   # 06:00 -> 14:00
    {"name": "Turno 3", "startHour": 14},  # 14:00 -> 22:00
]

# ===== Fin configuración =====

import system
from java.util import Date

def query_series(tagPath, startDate, endDate, intervalSeconds=1):
    """
    Consulta historial de un tag como lista [(ts, val)] usando LastValue y resample.
    """
    ds = system.tag.queryTagHistory(
        paths=[tagPath],
        startDate=startDate,
        endDate=endDate,
        returnSize=0,
        aggregationMode="LastValue",
        intervalSeconds=intervalSeconds,
        includeBoundingValues=True,
        usePollRate=True,
        returnFormat="Wide",
        ignoreBadQuality=True
    )
    out = []
    if ds is None or ds.getRowCount() == 0:
        return out
    for i in range(ds.getRowCount()):
        ts = ds.getValueAt(i, 0)  # java.util.Date
        val = ds.getValueAt(i, 1)
        out.append((ts, val))
    return out

def detect_density_changes(series):
    """
    Devuelve lista de dicts con cambios de SP:
    [{'t_change': Date, 'new_sp': x, 'old_sp': y}]
    """
    changes = []
    prev_val = None
    for ts, val in series:
        if prev_val is None:
            prev_val = val
            continue
        if val != prev_val:
            changes.append({"t_change": ts, "new_sp": val, "old_sp": prev_val})
            prev_val = val
    return changes

def find_downtime_intervals(status_series, value_stop=VAL_STOP, value_run=VAL_RUN):
    """
    Devuelve intervalos de paro (estado==value_stop) como:
    [{'start': Date, 'end': Date or None}]
    """
    intervals = []
    in_stop = False
    t_start = None
    last_val = None

    for ts, val in status_series:
        # Entrada a paro
        if not in_stop:
            if val == value_stop and last_val != value_stop:
                in_stop = True
                t_start = ts
        else:
            # Salida de paro
            if val == value_run:
                intervals.append({"start": t_start, "end": ts})
                in_stop = False
                t_start = None
        last_val = val

    # Paro abierto al final del rango
    if in_stop and t_start is not None:
        intervals.append({"start": t_start, "end": None})

    return intervals

def match_changes_to_downtimes(changes, intervals):
    """
    Para cada cambio de densidad, asigna el paro que:
    - Contiene el t_change (si el cambio cae dentro del paro), o
    - Es el primer paro que empieza en o después de t_change.
    Retorna lista con dicts:
    {'t_change', 'new_sp', 'old_sp', 'stop_start', 'stop_end', 'duration_ms'}
    """
    results = []
    for ch in changes:
        t = ch["t_change"]
        matched = None
        for it in intervals:
            s = it["start"]
            e = it["end"]
            if s is None:
                continue
            if e is not None:
                # Cambio dentro del paro, o el paro empieza después del cambio
                if (t.getTime() >= s.getTime() and t.getTime() <= e.getTime()) or (t.getTime() <= s.getTime()):
                    matched = it
                    break
            else:
                # Paro abierto
                if t.getTime() >= s.getTime():
                    matched = it
                    break

        if matched is not None:
            if matched["end"] is not None:
                duration_ms = matched["end"].getTime() - matched["start"].getTime()
            else:
                duration_ms = None
            results.append({
                "t_change": ch["t_change"],
                "new_sp": ch["new_sp"],
                "old_sp": ch["old_sp"],
                "stop_start": matched["start"],
                "stop_end": matched["end"],
                "duration_ms": duration_ms
            })
        else:
            results.append({
                "t_change": ch["t_change"],
                "new_sp": ch["new_sp"],
                "old_sp": ch["old_sp"],
                "stop_start": None,
                "stop_end": None,
                "duration_ms": None
            })
    return results

def build_shift_windows(startDate, endDate, turnos=TURNOS):
    """
    Construye ventanas de turno entre startDate y endDate.
    Retorna: [{'name', 'start', 'end'}]
    """
    windows = []
    sorted_turnos = sorted(turnos, key=lambda t: t["startHour"])

    dayStart = system.date.midnight(startDate)
    while dayStart.getTime() <= endDate.getTime():
        for idx, tdef in enumerate(sorted_turnos):
            name = tdef["name"]
            sh = tdef["startHour"]
            start = system.date.addHours(dayStart, sh)
            if idx < len(sorted_turnos) - 1:
                next_sh = sorted_turnos[idx + 1]["startHour"]
                end = system.date.addHours(dayStart, next_sh)
            else:
                next_day = system.date.addDays(dayStart, 1)
                first_sh = sorted_turnos[0]["startHour"]
                end = system.date.addHours(next_day, first_sh)

            # Recorte al rango
            if end.getTime() < startDate.getTime() or start.getTime() > endDate.getTime():
                continue
            s = start if start.getTime() >= startDate.getTime() else startDate
            e = end if end.getTime() <= endDate.getTime() else endDate
            windows.append({"name": name, "start": s, "end": e})
        dayStart = system.date.addDays(dayStart, 1)
    return windows

def find_shift_name_for_time(t, shift_windows):
    """
    Retorna el nombre del turno que contiene el instante 't'.
    Si no hay ventana (no debería), retorna None.
    """
    tms = t.getTime()
    for sw in shift_windows:
        if sw["start"].getTime() <= tms < sw["end"].getTime():
            return sw["name"]
    return None

def calcularParosPorCambioDensidad(startDate, endDate, intervalSeconds=1):
    """
    Función principal: devuelve DataSet con:
    Fecha (cambio) | Turno (inicio paro) | SP nuevo | SP anterior | Inicio Paro | Fin Paro | Min Paro | Observación
    """
    # 1) Consulta series
    sp_series = query_series(TAG_SP, startDate, endDate, intervalSeconds)
    estado_series = query_series(TAG_ESTADO, startDate, endDate, intervalSeconds)

    # 2) Cambios de densidad
    changes = detect_density_changes(sp_series)

    # 3) Intervalos de paro
    downtimes = find_downtime_intervals(estado_series, VAL_STOP, VAL_RUN)

    # 4) Asocia cambios a paros
    matched = match_changes_to_downtimes(changes, downtimes)

    # 5) Ventanas de turno para asignación por inicio del paro
    shift_windows = build_shift_windows(startDate, endDate, TURNOS)

    # 6) Arma filas (sin dividir por turnos: se asigna al turno del inicio del paro)
    rows = []
    for m in matched:
        obs = ""
        turno = None
        minutos = None

        if m["stop_start"] is None:
            obs = "Sin paro asociado al cambio"
        else:
            turno = find_shift_name_for_time(m["stop_start"], shift_windows)
            if m["stop_end"] is None:
                obs = "Paro sin cierre dentro del rango"
            else:
                minutos = round(m["duration_ms"] / 60000.0, 2) if m["duration_ms"] is not None else None

        rows.append([
            m["t_change"],   # ya es java.util.Date
            turno,
            m["new_sp"],
            m["old_sp"],
            m["stop_start"], # java.util.Date o None
            m["stop_end"],   # java.util.Date o None
            minutos,
            obs
        ])

    headers = ["Fecha", "Turno", "SP nuevo", "SP anterior", "Inicio Paro", "Fin Paro", "Min Paro", "Observación"]
    ds = system.dataset.toDataSet(headers, rows)
    return ds
    
    
    
    
    
