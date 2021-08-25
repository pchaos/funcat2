# -*- coding: utf-8 -*-
"""根据各券商connect.cfg文件，更新QA本地tdx ip配置文件
"""
import os
import datetime
import json
import random
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API
from QUANTAXIS.QAUtil import QASetting

__updated__ = "2021-08-25"


def ping_write_config(stock_ip_list, stock_ip_filename):
    """从配置文件读取通达信行情服务器信息，测试是否可用。不可用的ip删除。删除的ip保存在临时文件'/tmp/removed_ip.json'中
    """
    def _remove_element(element):
        print(f"del {element}")
        #  del element
        stock_ip_list.remove(element)
        remove_list.append(element)

    if len(stock_ip_list) == 0 and os.path.exists(stock_ip_filename):
        with open(stock_ip_filename, "r") as f:
            # print(f"from {stock_ip_filename}:{stock_ip_list}")
            stock_ip_list = json.load(f)
    remove_list = []
    for element in stock_ip_list:
        print(f"dealing :{element}")
        try:
            ping_time = ping(element["ip"], element["port"])
            if ping_time < datetime.timedelta(0, 1):
                print(element["ip"], element["port"])
                element["pingtime"] = ping_time.microseconds
            else:
                _remove_element(element)
        except Exception as e:
            _remove_element(element)

    print(f"finished ping : {stock_ip_list}")
    try:
        print(f"saving {stock_ip_filename}")
        write_quantaxis_config(f"{stock_ip_filename}", stock_ip_list)
        if len(remove_list) > 0:
            write_quantaxis_config("/tmp/removed_ip.json", remove_list)
    except Exception as e:
        print(e)
        print(stock_ip_list)


# ping失败标记
__badtime = datetime.timedelta(9, 9, 0)


def ping(ip, port=7709, type_='stock'):
    api = TdxHq_API()
    apix = TdxExHq_API()
    __time1 = datetime.datetime.now()
    try:
        if type_ in ['stock']:
            with api.connect(ip, port, time_out=0.9):
                res = api.get_security_list(0, 1)

                if res is not None:
                    if len(api.get_security_list(0, 1)) > 800:
                        return datetime.datetime.now() - __time1
                    else:
                        print('BAD RESPONSE {}'.format(ip))
                        return __badtime
                else:
                    print('BAD RESPONSE {}'.format(ip))
                    return __badtime
        elif type_ in ['future']:
            with apix.connect(ip, port, time_out=0.7):
                res = apix.get_instrument_count()
                if res is not None:
                    if res > 20000:
                        return datetime.datetime.now() - __time1
                    else:
                        print(f'️Bad FUTUREIP REPSONSE {ip}')
                        return __badtime
                else:
                    print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                    return __badtime
    except Exception as e:
        if isinstance(e, TypeError):
            print(e)
            print(ip, port)
            print('Tushare内置的pytdx版本和QUANTAXIS使用的pytdx 版本不同, 请重新安装pytdx以解决此问题')
            print('pip uninstall pytdx')
            print('pip install pytdx')

        else:
            print('BAD RESPONSE {}'.format(ip))
        return __badtime


def read_tdx_config(filename: str = ""):
    import configparser
    if not os.path.exists(filename):
        print(F"file not exists: {filename}")
        return []
    config = configparser.ConfigParser()
    # tdx配置文件使用的是GBK编码
    config.read(f'{filename}', encoding='GBK')
    tdx = []
    hqhost = config['HQHOST']
    hostn = int(config['HQHOST']['HostNum'])
    for i in range(1, hostn + 1):
        name = hqhost[f"HostName{i:02d}"]
        ip = hqhost[f"IPAddress{i:02d}"]
        port = hqhost[f"Port{i:02d}"]
        tdx.append({"ip": ip, "name": name, "port": int(port)})
    return tdx


def write_quantaxis_config(filename: str = "", data: json = {}):
    with open(filename, 'w') as data_file:
        # Save non-ASCII or Unicode data as-is not as \u escape sequence in
        # JSON
        data_file.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_stock_ips():
    from multiprocessing import cpu_count
    from QUANTAXIS.QAFetch.QATdx import get_ip_list_by_multi_process_ping
    ips = get_ip_list_by_multi_process_ping(stock_ip_list, _type='stock')[
        :cpu_count() * 2 + 1]
    return ips


def get_mainmarket_ip(ip, port):
    """[summary]
    Arguments:
        ip {[type]} -- [description]
        port {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    global best_ip
    if ip is None and port is None:
        ips = get_stock_ips()
        n = len(ips)
        if n > 0:
            item = ips[random.randint(0, n - 1)]
            ip = item['ip']
            port = item['port']
    else:
        pass
    return ip, port


if __name__ == "__main__":

    stock_ip_list = QASetting.stock_ip_list
    print(f"{len(stock_ip_list)=}\n{json.dumps(stock_ip_list, indent=4)}")

    # stock ip list file
    stock_ip_filename = QASetting.STOCK_IP_FILE_PATH

    # 从通达信config文件中添加行情ip
    currDir = os.path.join(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."), "datas")
    print(currDir)
    connects = ['connect.cfg',
                'tdxnew_connect.cfg',
                'caitong_connect.cfg',
                ]
    for connect_file in connects:
        tdx_config = read_tdx_config(os.path.join(currDir, connect_file))
        print(tdx_config)
        print(
            f"before add tdx_config {len(stock_ip_list)=}\n{json.dumps(stock_ip_list, indent=4)}")
        for element in tdx_config:
            if element not in stock_ip_list:
                print(f"add {element}")
                stock_ip_list.append(element)
    print(f"{len(stock_ip_list)=}\n{json.dumps(stock_ip_list, indent=4)}")
    ping_write_config(stock_ip_list, stock_ip_filename)
    ips = get_stock_ips()
    print(f"{ips=}")

    for i in range(10):
        print(get_mainmarket_ip(None, None))
