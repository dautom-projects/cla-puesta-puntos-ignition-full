SELECT  [Table] , DUFWRev , [Group] , FormProg , FormHrs , RefillAcid , BathLevel , Priority

FROM currentSchedule
where  ItemID = :table and StatusID = 2
order by StatusID asc, StartDate asc