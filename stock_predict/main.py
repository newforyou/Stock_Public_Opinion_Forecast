
import re
import requests
import json
from bs4 import BeautifulSoup


# 将text按照lenth长度分为不同的几段
def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr  # 返回多段值


def get_emotion(data):
    # 定义百度API情感分析的token值和URL值
    token = '24.a73afc0203b60ebf4c5711a207a698af.2592000.1680751530.282335-31034216'
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)
    if (len(data.encode()) < 2048):
        new_each = {'text': data}  # 将文本数据保存在变量new_each中，data的数据类型为string
        new_each = json.dumps(new_each)
        res = requests.post(url, data=new_each)  # 利用URL请求百度情感分析API
        res_text = res.text  # 保存分析得到的结果，以string格式保存
        print("content: ", res_text)
        result = res_text.find('items')  # 查找得到的结果中是否有items这一项
        positive = 1
        if (result != -1):  # 如果结果不等于-1，则说明存在items这一项
            json_data = json.loads(res.text)
            negative = (json_data['items'][0]['negative_prob'])  # 得到消极指数值
            positive = (json_data['items'][0]['positive_prob'])  # 得到积极指数值
            print("positive:", positive)
            print("negative:", negative)
            if (positive > negative):  # 如果积极大于消极，则返回2
                return 2
            elif (positive == negative):  # 如果消极等于积极，则返回1
                return 1
            else:
                return 0  # 否则，返回0
        else:
            return 1
    else:
        print("文章切分")
        data = cut_text(data, 1500)  # 如果文章字节长度大于1500，则切分
        sum_positive = 0.0  # 定义积极指数值总合
        sum_negative = 0.0  # 定义消极指数值总和
        for each in data:  # 遍历每一段文字
            new_each = {
                'text': each  # 将文本数据保存在变量new_each中
            }
            new_each = json.dumps(new_each)
            res = requests.post(url, data=new_each)  # 利用URL请求百度情感分析API
            res_text = res.text  # 保存分析得到的结果，以string格式保存
            result = res_text.find('items')
            if (result != -1):
                json_data = json.loads(res.text)  # 如果结果不等于-1，则说明存在items这一项
                positive = (json_data['items'][0]['positive_prob'])  # 得到积极指数值
                negative = (json_data['items'][0]['negative_prob'])  # 得到消极指数值
                sum_positive = sum_positive + positive  # 积极指数值加和
                sum_negative = sum_negative + negative  # 消极指数值加和
            print(sum_positive)
            print(sum_negative)
            if (sum_positive > sum_negative):  # 积极 如果积极大于消极，则返回2
                return 2
            elif (sum_positive == sum_negative):  # 中性 如果消极等于于积极，则返回1
                return 1
            else:
                return 0  # 消极，返回0


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'

    }  # 模拟浏览器访问
    response = requests.get(url, headers=headers)  # 请求访问网站
    html = response.text  # 获取网页源码
    soup = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup库,并设置解析器
    a = soup.select('p')
    text = ""
    for i in a:
        text = text + i.text
    return text


def main():
    txt1 = get_html("https://baijiahao.baidu.com/s?id=1680186652532987655&wfr=spider&for=pc")
    print(txt1)
    print("txt1测试结果：", get_emotion(txt1))


if __name__ == "__main__":
    main()

