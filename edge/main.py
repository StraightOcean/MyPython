import json
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# 设置 WebDriver 路径
driver_path = "bin/msedgedriver.exe"

# 配置反检测选项
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

service = Service(executable_path=driver_path)

try:
    driver = webdriver.Edge(service=service, options=options)

    # 隐藏自动化特征
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en']
        });
        """
    })

    print("浏览器启动成功，开始模拟人类行为...")

    # 访问目标网站
    driver.get("https://cn.bing.com/")
    time.sleep(random.uniform(2, 4))  # 随机等待

    print("页面标题:", driver.title)

    for _ in range(20):
        resource = requests.get("https://wapi.wangyupu.com/api/nng")
        data = json.loads(resource.text)

        search_box = driver.find_element(By.NAME, "q")

        time.sleep(random.uniform(0.1, 0.3))
        search_box.clear()
        for char in data['name']:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))# 随机打字间隔

        search_box.send_keys(Keys.RETURN)

        print("页面标题:", driver.title)
        sleep(1)

        # 创建动作链对象
        actions = ActionChains(driver)

        print("开始模拟鼠标滚动行为...")

        # 模拟向下滚动（分多次，模拟人类行为）
        scroll_steps_down = random.randint(8, 15)  # 随机滚动次数
        for i in range(scroll_steps_down):
            # 随机滚动距离（像素）
            scroll_distance = random.randint(100, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

            # 随机停顿时间
            pause_time = random.uniform(0.1, 0.8)
            time.sleep(pause_time)

            if i % 3 == 0:  # 每隔几次稍微停留长一点
                time.sleep(random.uniform(0.5, 1.5))

            print(f"向下滚动第 {i+1} 次，距离: {scroll_distance}px")

        # 在底部停留一会儿
        time.sleep(random.uniform(1, 3))
        print("到达页面底部，准备返回...")

        # 模拟向上滚动返回
        scroll_steps_up = random.randint(6, 12)
        for i in range(scroll_steps_up):
            scroll_distance = random.randint(150, 350)
            driver.execute_script(f"window.scrollBy(0, -{scroll_distance});")

            pause_time = random.uniform(0.1, 0.6)
            time.sleep(pause_time)

            if i % 2 == 0:
                time.sleep(random.uniform(0.3, 1.0))

            print(f"向上滚动第 {i+1} 次，距离: {scroll_distance}px")

        # 回到顶部后稍作停留
        time.sleep(random.uniform(1, 2))
        print("已回到页面顶部")


finally:
    print("正在关闭浏览器...")
    driver.quit()
    print("程序执行完毕")
