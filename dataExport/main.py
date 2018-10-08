import pymysql
import csv
import codecs

def get_db_conn():
	conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',database='battery1')
	return conn


def query_all(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchall()


def read_mysql_to_csv(filename):
    with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
        write = csv.writer(f, dialect='excel')
        conn = get_db_conn()
        cur = conn.cursor()
        sql = 'select * from apps_celltesthistorydatatable'
        results = query_all(cur=cur, sql=sql, args=None)
        for result in results:
            print(result)
            write.writerow(result)



if __name__ == '__main__':
    read_mysql_to_csv('1.csv')
