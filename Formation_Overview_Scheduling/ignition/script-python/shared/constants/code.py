#Common repository for shared constants
SOURCE_PATH = "Formation/Tables"
LINE_NAME_1 = "Oriental"
LINE_NAME_2 = "Occidental"
LINE_MIN_TABLE_1 = 1
LINE_MAX_TABLE_1 = 9
LINE_MIN_TABLE_2 = 10
LINE_MAX_TABLE_2 = 18
DATA_PATH = "[default]Formation/Tables"
InitConst1 = "[default]Formation/Lockup Tool/LoadTableTime"
InitConst2 = "[default]Formation/Lockup Tool/NormalTableTime"
CALC_FOLDER = "[default]Formation/Lockup Tool/Line "
EMPTY_STATES = ['0','1','11', '999']
PROJECT_NAME = "Formation_Overview_Scheduling"
from FST import namedQueries
QS11 = namedQueries.getTableLineQuery1(1)
QS12 = namedQueries.getTableLineQuery2(1)
QS21 = namedQueries.getTableLineQuery1(2)
QS22 = namedQueries.getTableLineQuery2(2)
QST1 = namedQueries.getTableLineQuery1(3)
QST2 = namedQueries.getTableLineQuery2(3)
