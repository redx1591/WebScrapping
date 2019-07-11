from __future__ import print_function
import mysql.connector


def insert(user, passW, host, dbname, data,cmd_sql):
    cnx = mysql.connector.connect(user=user, password=passW, host=host, database=dbname)

    cursor = cnx.cursor()

    # Insert data
    for d in data:
        try:
            cursor.execute(cmd_sql, d)
        except:
            pass

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()

    return cnx.close()


'''Function for products insertion'''
def insertProduct(user, passW, host, dbname, produits):

    cmd_sql = ("INSERT INTO "+"products"
               "(id,libProduct,slug,descProduct,priceProduct,imgProduct,numSeller,src,urlProduct,logo,logoS,origin)"
               "VALUES (%(id)s,%(libProduct)s,%(slug)s,%(descProduct)s,%(priceProduct)s,%(imgProduct)s,%(numSeller)s,%(src)s,%(urlProduct)s,%(logo)s,%(logoS)s,%(origin)s)")

    '''Insertion of products'''

    insert(user, passW, host, dbname, produits, cmd_sql)

    return True

