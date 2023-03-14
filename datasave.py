"""
对获取到的数据进行清洗
并把数据存入mysql数据库
"""
import json
import pymysql



def save_to_stock(stockId,ts_code,name,industry,list_date,area,predict,real):
    con=pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="164606963",
        db="stock"
    )
    db=con.cursor()
    sql=f'insert into stock(`stockId`,`ts_code`,`name`,`industry`,`list_date`,`area`,`predict`,`real`)values("{stockId}","{ts_code}","{name}","{industry}","{list_date}","{area}","{predict}","{real}")'
    db.execute(sql)
    con.commit()
    db.close()

with open('companyProfile.json','r',encoding='utf8')as fp:
    json_data=json.load(fp)

list_ts_code=[]
list_stockId=[]
list_name=[]
list_industry=[]
list_list_date=[]
list_area=[]


dic_ts_code=json_data.get("ts_code")
for key in dic_ts_code.keys():
    list_ts_code.append(dic_ts_code[key])

dic_stockId=json_data.get("symbol")
for key in dic_stockId.keys():
    list_stockId.append(dic_stockId[key])

dic_name=json_data.get("name")
for key in dic_name.keys():
    list_name.append(dic_name[key])

dic_industry=json_data.get("industry")
for key in dic_industry.keys():
    list_industry.append(dic_industry[key])

dic_list_date=json_data.get("list_date")
for key in dic_list_date.keys():
    upto_date=dic_list_date[key][:4]+"-"+dic_list_date[key][5:6]+"-"+dic_list_date[key][7:8]
    list_list_date.append(upto_date)

dic_area=json_data.get("area")
for key in dic_area.keys():
    list_area.append(dic_area[key])

for i in range(0,20):
    stockId=list_stockId[i]
    ts_code=list_ts_code[i]
    name=list_name[i]
    industry=list_industry[i]
    list_date=list_list_date[i]
    area=list_area[i]
    with open("./stock_predict/predict_Data/" +ts_code+ "_predict.txt", 'r', encoding='utf8') as fp:
        myline = []
        lines = fp.readlines()
        for line in lines:
            myline.append(line[:4])
        predict=','.join(myline)
        print(predict)
        print(type(predict))


    with open("./stock_predict/real_Data/" +ts_code+ "_real.txt", 'r', encoding='utf8') as fm:
        mylinereal = []
        linesreal = fm.readlines()
        for linere in linesreal:
            mylinereal.append(linere[:4])
        real=','.join(mylinereal)
        print(real)
        print(type(real))

    save_to_stock(stockId=stockId, ts_code=ts_code, name=name, industry=industry, list_date=list_date,area=area,predict=predict,real=real)


