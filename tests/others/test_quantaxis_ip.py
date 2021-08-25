# -*- coding: utf-8 -*-
from QUANTAXIS.QAUtil import QASetting

stock_ip_list= QASetting.stock_ip_list
print(stock_ip_list)

# stock ip list file
stock_ip_file = QASetting.STOCK_IP_FILE_PATH
if os.path.exists(stock_ip_file):
    with open(stock_ip_file, "r") as f:
        stock_ip_list = json.load(f)

