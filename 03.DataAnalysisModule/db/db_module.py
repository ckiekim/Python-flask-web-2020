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

def get_region_items_by_gubun_with_date(items, gubun, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from region where gubun=? and stdDay between ? and ?;'
    cur.execute(sql, (gubun, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_agender_items_by_gubun(items, gubun):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from agender where gubun=?;'
    cur.execute(sql, (gubun,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_agender_items_by_gubun_with_date(items, gubun, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from agender where gubun=? and stdDay between ? and ?;'
    cur.execute(sql, (gubun, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_seoul_items_by_gu(items, gu):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from seoul where region=?;'
    cur.execute(sql, (gu,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_seoul_items_by_condition(items, gu, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from seoul where region=? and confDay between ? and ?;'
    cur.execute(sql, (gu, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_seoul_last_sid():
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select sid from seoul order by sid desc limit 1;'
    cur.execute(sql)
    row = cur.fetchone()
    
    cur.close()
    conn.close()
    return row[0]

def insert_seoul_data(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'insert into seoul values(?,?,?,?,?,?,?);'
    cur.execute(sql, params)
    conn.commit()
    
    cur.close()
    conn.close()
    return

def insert_seoul_bulk_data(df):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'insert into seoul values(?,?,?,?,?,?,?);'
    for i in df.index:
        params = [int(df.iloc[i,0])]
        params.extend(df.iloc[i,1:])
        cur.execute(sql, params)
        if i % 100 == 0:
            conn.commit()
    conn.commit()
    
    cur.close()
    conn.close()
    return