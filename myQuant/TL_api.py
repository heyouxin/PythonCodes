# -*- coding: utf-8 -*-
from dataapi import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('a9bd16e6728445fcc3168ef5729284aa5c27123a64b2fd2fec047ead1e7b7749')
        url1='/api/equity/getEquManagersInfo.json?field=&secID=&ticker=000001'
        code, result = client.getData(url1)
        if code==200:
            print(result)
        else:
            print(code)
            print(result)
            '''
        url2='/api/equity/getSecST.csv?field=&secID=&ticker=000521&beginDate=20020101&endDate=20150828'
        code, result = client.getData(url2)
        if(code==200):
            file_object = open('thefile.csv', 'w')
            file_object.write(result)
            file_object.close( )
        else:
            print(code)
            print result)
            '''
    except Exception as e:
        #traceback.print_exc()
        print(e)
        