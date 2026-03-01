from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import os
import requests
import json

# 设置 WebDriver 路径
driver_path = "bin/msedgedriver.exe"

# 获取当前用户的 Edge 用户数据目录
user_profile = os.path.expanduser("~")
edge_user_data = os.path.join(user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data")

# 配置 Edge 选项
options = Options()
options.add_argument(f"--user-data-dir={edge_user_data}")
options.add_argument("--profile-directory=Default")
# 添加这些参数来避免冲突
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--headless")

service = Service(executable_path=driver_path)
driver = webdriver.Edge(service=service, options=options)

try:
    # 打开 Bing
    driver.get("https://cn.bing.com/")

    # 等待页面加载
    time.sleep(3)

    # 进行搜索
    for _ in range(20):
        resource = requests.get("https://wapi.wangyupu.com/api/nng")
        data = json.loads(resource.text)

        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(data['name'])
        search_box.send_keys(Keys.RETURN)

        print("页面标题:", driver.title)
        sleep(1)

finally:
    driver.quit()
