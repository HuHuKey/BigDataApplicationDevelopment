import requests
from http.cookiejar import CookieJar

# 创建一个会话对象，它会自动处理cookie
session = requests.Session()

# 创建一个CookieJar对象
cookiejar = CookieJar()

# 将CookieJar对象与会话关联
session.cookies = cookiejar

# 发送请求到目标网页
url = 'https://search.jd.com/'  # 替换为你要获取cookie的网址
response = session.get(url)

# 打印获取到的cookie
for cookie in cookiejar:
    print(f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain}")