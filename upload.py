import psycopg2
import csv
import itertools

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

con = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="40.118.124.20", port="5432")

print("Database opened successfully")

cur = con.cursor()
cur.execute("SELECT * from receipt")
rows = cur.fetchall()

print(len(rows))

cur = con.cursor()


with open('/home/nikita/Junction-Kesko-Receipt-Data/Junction_data.csv') as f:
    spamreader = csv.reader(f, delimiter=';', quotechar='"')
    print('file read')
    i = 0

    step = 100000
    current = 0
    chunks = grouper(spamreader, step)
    for chunk in chunks:
        if i == 0:
            i += 1
            continue
        rows = ""
        for row in chunk:
            single_row = f"""({row[0]}, {row[1]}, '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', {row[7]}, '{row[8]}', '{row[9]}')"""
            if single_row is None:
                continue
            rows += single_row
            rows += ','
        rows = rows[:-1]
        query = f"""
        INSERT INTO receipt (AreaId,Receipt,TransactionDate,BeginHour,EAN,Quantity,PersonAgeGrp,KCustomer,QualClass,EasyClass) VALUES {rows};"""
        cur.execute(query)
        current += step
        print(current)
        if current % (step * 10) == 0:
            print("commit")
            con.commit()
    con.commit()
    # for row in spamreader:
    #     if i == 0:
    #         i += 1
            
    #         continue
    #     single_row = f"""(
    #         {row[0]}, 
    #         {row[1]}, 
    #         '{row[2]}', 
    #         '{row[3]}', 
    #         '{row[4]}', 
    #         '{row[5]}', 
    #         '{row[6]}', 
    #         {row[7]}, 
    #         '{row[8]}', 
    #         '{row[9]}'
    #     )"""
        
    #     query = f"""
    #     INSERT INTO receipt (AreaId,Receipt,TransactionDate,BeginHour,EAN,Quantity,PersonAgeGrp,KCustomer,QualClass,EasyClass) VALUES {single_row}"""
    #     print(i)
    #     i += 1
    #     
        


