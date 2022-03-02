import requests


proxy_pool_url = 'http://localhost:5000/random'


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


proxy = get_proxy()
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' +proxy

}
try:
    response = requests.get('http://www.bing.com', proxies=proxies, timeout=8)
    with open('test.html', 'wb')as f:
        f.write(response.content)
    print(response.status_code)
except:
    print("Error...")