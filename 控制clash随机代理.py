import random

import requests
from concurrent.futures import ThreadPoolExecutor


class Clash():
    def __init__(self, url, secret):
        self.url = url
        self.secret = secret
        self.header = {'Authorization': f'Bearer {self.secret}'}
        self.all_proxies = []
        self.active_proxies = []
        self.Selectors = []
        self.get_all_proxies()
        # self.update_active_proxies()
        # print(f'初始化成功，可用的代理数量有{len(self.active_proxies)}个')

    def get_all_proxies(self):
        res = requests.get(f'{self.url}/proxies', headers=self.header).json()
        for key, value in res['proxies'].items():
            if value['type'] == 'Shadowsocks':
                self.all_proxies.append(key)

    def update_active_proxies(self):
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.get_delay, self.all_proxies)
        for proxy_name, delay in zip(self.all_proxies, results):
            if delay:
                self.active_proxies.append(proxy_name)
        return True

    def get_delay(self, proxy_name, timeout=500, url='https://www.gstatic.com/generate_204'):
        params = {"timeout": timeout, "url": url}
        res = requests.get(f'{self.url}/proxies/{proxy_name}/delay', headers=self.header, params=params)
        try:
            if 'timeout' not in res.text and 'delay' in res.text:
                return res.json()['delay']
        except:
            pass
        return False

    def random_proxy(self, timeout=500,_name='🔰国外流量'):
        while True:
            proxy_name = random.choice(self.all_proxies)
            delay = self.get_delay(proxy_name=proxy_name, timeout=timeout)
            if delay:
                break
        res = requests.put(f'{self.url}/proxies/{_name}', headers=self.header, json={"name": proxy_name})
        if res.ok:
            print(f'成功切换到：{proxy_name},延迟{delay}ms')
        else:
            print(f'切换失败，{res.text}')

    # 修改配置
    def set_config(self,mode='Global'):
        data_json = {
            "mode": mode # Rule
        }
        res = requests.patch(f'{self.url}/configs', headers=self.header, json=data_json)
        print(res.text)
        if res.ok:
            print(f'成功切换到：{mode}')
        else:
            print(f'切换失败，{mode}')


if __name__ == '__main__':
    url = 'http://127.0.0.1:51991'
    secret = 'a6fe2579-c401-47c3-a97c-0e0af9c0746d'
    _clash = Clash(url, secret)
    _clash.set_config('Global')#Rule
    # _clash.get_all_proxies()
    # print(_clash.Selectors)
    for i in range(1):
        _clash.random_proxy(1000,'GLOBAL')
        res = requests.get('https://icanhazip.com/').text
        print(res)
