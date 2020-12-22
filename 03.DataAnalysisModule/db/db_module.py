import sqlite3

def get_region_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'select * from region where stdDay=? order by incDec desc;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def write_region(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    #print(params)
    sql = '''insert into region(stdDay, deathCnt, defCnt, gubun, incDec, isolClearCnt,
             isolIngCnt, localOccCnt, overFlowCnt, qurRate) values(?,?,?,?,?,?,?,?,?,?);'''
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()
    return

def get_agender_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'select * from agender where stdDay=?;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def write_agender(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    #print(params)
    sql = '''insert into agender(stdDay, confCase, confCaseRate, death, deathRate,
             criticalRate, gubun, seq, updateDt) values(?,?,?,?,?,?,?,?,?);'''
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()
    return

def get_region_items_by_gubun(items, gubun):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from region where gubun=?;'
    cur.execute(sql, (gubun,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

