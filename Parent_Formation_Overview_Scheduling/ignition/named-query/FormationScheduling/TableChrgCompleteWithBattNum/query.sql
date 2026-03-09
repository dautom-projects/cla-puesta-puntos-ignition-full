SELECT CONVERT(VARCHAR(14), t_stamp, 113), TableChargingData.[Table 1],TableChargingData.[Table 2],TableChargingData.[Table 3],TableChargingData.[Table 4],TableChargingData.[Table 5],  
TableChargingData.[Table 6],TableChargingData.[Table 7],TableChargingData.[Table 8],TableChargingData.[Table 9],TableChargingData.[Table 10],
TableChargingData.[Table 11],TableChargingData.[Table 12],TableChargingData.[Table 13],TableChargingData.[Table 14],TableChargingData.[Table 15],  
TableChargingData.[Table 16],TableChargingData.[Table 17],TableChargingData.[Table 18],TableChargingData.[Table 21],TableChargingData.[Table 22],TableChargingData.[Table 23],TableChargingData.[Table 24],TableChargingData.[Table 25],  
TableChargingData.[Table 26],TableChargingData.[Table 27],TableChargingData.[Table 28],TableChargingData.[Table 29],TableChargingData.[Table 30],TableChargingData.[Table 31],TableChargingData.[Table 32],
TableChargingData.[Table 33],TableChargingData.[Table 34]
FROM TableChargingData
WHERE (t_stamp BETWEEN '{Root Container.SearchHour}' AND '{Root Container.LastHour}') 
GROUP BY
  CONVERT(VARCHAR(14), t_stamp, 113),TableChargingData.[Table 1],TableChargingData.[Table 2],TableChargingData.[Table 3],TableChargingData.[Table 4],TableChargingData.[Table 5],  
TableChargingData.[Table 6],TableChargingData.[Table 7],TableChargingData.[Table 8],TableChargingData.[Table 9],TableChargingData.[Table 10],
TableChargingData.[Table 11],TableChargingData.[Table 12],TableChargingData.[Table 13],TableChargingData.[Table 14],TableChargingData.[Table 15],  
TableChargingData.[Table 16],TableChargingData.[Table 17],TableChargingData.[Table 18],TableChargingData.[Table 21],TableChargingData.[Table 22],TableChargingData.[Table 23],TableChargingData.[Table 24],TableChargingData.[Table 25],  
TableChargingData.[Table 26],TableChargingData.[Table 27],TableChargingData.[Table 28],TableChargingData.[Table 29],TableChargingData.[Table 30],TableChargingData.[Table 31],TableChargingData.[Table 32],
TableChargingData.[Table 33],TableChargingData.[Table 34]
  
 order by   CONVERT(VARCHAR(14), t_stamp, 113) asc