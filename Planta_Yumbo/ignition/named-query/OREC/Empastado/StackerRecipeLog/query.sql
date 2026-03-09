SELECT 
    Linea,
    PlateID,
    Timestamp,
    Elevators_Home,
    Elevators_Transfer_Pos,
    Exit_Conveyor_Speed,
    Forks_Home,
    Forks_Step_Down,
    Grid_Weight,
    PlatePerStack,
    Plates_Change_Fork_to_Elev,
    Plates_to_Step,
    Servos_Position_Tol,
    Spreader_Speed,
    Tamper_Speed,
    Thickness,
    Weight
FROM StackerRecipeLog
WHERE (:linea IS NULL OR Linea = :linea)
ORDER BY Timestamp DESC;
