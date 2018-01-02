# -*- coding: utf-8 -*-
from dataapi import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init("a9bd16e6728445fcc3168ef5729284aa5c27123a64b2fd2fec047ead1e7b7749")
        url1="/api/equity/getEqu.csv?field=&listStatusCD=&secID=&ticker=&equTypeCD=A"
        code, result = client.getData(url1)
        if(code==200):
            print(str(result))
            file_object = open('thefile.csv', 'w')
            #file_object.write(str(result))
            file_object.close()
        else:
            print (code)
            print (result)
    except Exception as e:
        #traceback.print_exc()
        print(e)