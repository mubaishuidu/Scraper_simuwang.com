from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas
import time
import re
from lxml import html
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains     

driver = webdriver.Chrome()         # 启动驱动器

#防检测
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get('https://simu.howbuy.com/ruiputouzi/SD7791/')
driver.maximize_window()
time.sleep(600)
