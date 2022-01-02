import re

# import dateparser


def get_eating_account(from_user, description, time=None):
    if time == None or not hasattr(time, 'hour'):
        return 'Expenses:Eatingdescriptions:Others'
    elif 6 <= time.hour <= 9:  # breakfast
        return 'Expenses:Food:Huawei'
    elif 11 <= time.hour <= 13:  # lunch
        return 'Expenses:Food:Huawei'
    elif 17 <= time.hour <= 19:
        return 'Expenses:Eating:Lunch'
    else:
        return 'Expenses:Eating:Supper'


def get_credit_return(from_user, description, time=None):
    for key, value in credit_cards.items():
        if key == from_user:
            return value
    return "Unknown"


public_accounts = [
    'Assets:Company:Alipay:StupidAlipay'
]

credit_cards = {
    '中信银行': 'Liabilities:CreditCard:CITIC',
}

accounts = {
    "余额宝": 'Assets:AliPay',
    '交通银行(9283)': 'Liabilities:CreditCard:BOCOM:9283',
    '交通银行信用卡(9283)': 'Liabilities:CreditCard:BOCOM:9283',
    '花呗': 'Liabilities:Alipay:Huabei',
    '建设银行(3832)': 'Liabilities:CreditCard:CCB:3832',
    '工商银行(7079)': 'Assets:Card:ICBC:7079',
    '中国工商银行储蓄卡(7079)':'Assets:Card:ICBC:7079',
    '零钱': 'Assets:WeChat',
    '/': 'Income:Other', 
}

descriptions = {
    # '滴滴打车|滴滴快车': get_didi,
    '余额宝.*收益发放': 'Assets:AliPay',
    # '转入到余利宝': 'Assets:Bank:MyBank',
    # '微信红包': 'Assets:WeChat',
    '花呗收钱服务费': 'Expenses:Fee',
    '自动还款-花呗.*账单': 'Liabilities:Alipay:Huabei',
    '信用卡自动还款|信用卡还款': get_credit_return,
    '.*外卖订单.*': 'Expenses:Food:TakeOut',
    '美团订单-骑行结费': 'Expenses:Transport:Bike',
    '深圳交通卡发行及充值': 'Expenses:Transport:Card',
    '地铁出行': 'Expenses:Transport:Subway',
    '火车票': 'Expenses:Transport:Train',
    '退款-火车票': 'Expenses:Transport:Train',
    '中国电信': 'Expenses:Life:Phone',
    "手机充值":'Expenses:Life:Phone',
    "深圳-D区.*":'Expenses:Food:Huawei',
    "点餐订单.*":"Expenses:Food:TakeOut",
    "深圳地铁":"Expenses:Transport:Subway"
}

anothers = {
    "丰巢科技":'Expenses:Transport:Postage',
    '上海拉扎斯': get_eating_account,
    'T3出行':'Expenses:Transport:Taxi',
    '江西电信.*':'Expenses:Life:Phone',
    '秦云老太婆摊摊面':'Expenses:Food:Huawei',
    '广东赛壹便利店有限公司':'Expenses:Food:Huawei',
    '中味餐饮华为D区店':'Expenses:Food:Huawei',
    '巷栖':'Expenses:Food:Huawei',
    '陈进': 'Expenses:Fun:Sports',
    '乡谷村': 'Expenses:Food:Huawei',
    '爱碗亭': 'Expenses:Food:Huawei',
    '.*东旭.*': 'Expenses:Food:Huawei',
    '.*徳堡澜餐饮.*': 'Expenses:Food:Huawei',
    '喜家德': 'Expenses:Food:Huawei',
    '家乐缘': 'Expenses:Food:Huawei',
    '井冈印象餐饮': 'Expenses:Food:Huawei',
    'apple': 'Expenses:Digital:Subscription',
    '怪兽充电': 'Expenses:Fun:Other',
    '志合护肤造型慢城店中心': 'Expenses:Life:Hair'
}

incomes = {
    '余额宝.*收益发放': 'Income:Other',
}

description_res = dict([(key, re.compile(key)) for key in descriptions])
another_res = dict([(key, re.compile(key)) for key in anothers])
income_res = dict([(key, re.compile(key)) for key in incomes])
