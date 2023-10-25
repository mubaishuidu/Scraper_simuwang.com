from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas
import time
import re
from lxml import html
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains        # 导入鼠标事件库
def login(): #登陆
  driver.find_element(By.XPATH,'//button[@class="comp-login-method comp-login-b2"]').click()      #点击账号密码登录
  driver.find_element(By.XPATH,'//input[@name="username"]').send_keys('15724746224')      # 输入账号
  driver.find_element(By.XPATH,'//input[@placeholder="请输入密码"]').send_keys('abcdefg123')        # 输入密码
  driver.find_element(By.XPATH,'//button[@class="comp-login-btn"]').click()            # 点击登录
  time.sleep(2)		# 加载网页需要等待时间


def getHideIds(htmlEtree): #找到隐藏的属性值
    encode_styles = "".join(htmlEtree.xpath('//div[@id="ENCODE_STYLE"]/style/text()')).replace("\n", "")
    # 清洗数据，去除连续的空格
    new_encode_styles = re.sub("  +", "", encode_styles)
    # 获取全部被隐藏的id
    hideIds1 = re.findall("\.(\w+) {font: 0/0 a;", new_encode_styles)  # 格式化后的html
    hideIds2 = re.findall("\.(\w+){font: 0/0 a;", new_encode_styles)  # 未格式化的html
    result = set(hideIds1 + hideIds2)
    return result


def getData(ln,attr):
    result = driver.find_element(By.XPATH,"((//div[@class='privateOpt']//div[@class='privateContent'])["+str(ln)+"])//div[@class='"+str(attr)+"']").text
    return result


driver = webdriver.Chrome()         # 启动驱动器

#防检测
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get('https://www.simuwang.com')
driver.maximize_window()

login()
#time.sleep(40)
mouse = driver.find_element(By.XPATH,'//div[@class="comp-header-nav-item fz14"]/div/span[@class="ellipsis"]')
ActionChains(driver).move_to_element(mouse).perform()
driver.find_element(By.XPATH,'//a[@class="comp-header-user-item icon-trade"]').click()
time.sleep(2)

page = driver.page_source
soup = BeautifulSoup(page,'html.parser')
list_name = []  # 用于保存目标名称
url_a = soup.select('div:nth-child(2) > div.shortName > a')    # 找到所爬取的网页
names = soup.select('div> div > div:nth-child(2) > div.shortName > a')  # 找到名称
for name in names:
    list_name.append(name.get_text())

data = {}
IDdata = {}
newDate = driver.find_element(By.XPATH,'((//div[@class="privateOpt"]//div[@class="privateContent"])[1]//div[@class="newNetTime"])[1]').text

try:
    netVal = pandas.read_csv("paipaiwang.csv")
    for n in netVal['names']:
        data[n] = ""
        IDdata[n] = ""
except:
    netVal = pandas.DataFrame()

for i in range(len(list_name)):
    shortName = getData(i+1,"shortName")
    newNet = getData(i+1,"newNet")
    data[shortName]=newNet
    
    driver.find_element(By.XPATH,"((//div[@class='privateOpt']//div[@class='privateContent'])["+str(i+1)+"])//div[@class='shortName']").click()
    time.sleep(5)
    IDnum = driver.find_element(By.XPATH,"//span[contains(text(),'备案')]//following-sibling::*").text
    IDdata[shortName]= IDnum
    driver.back()
    time.sleep(3)
    
print("HELLO")
netVal['names'] = data.keys()
netVal['ID'] = IDdata.keys()
netVal[newDate] = data.values()

netVal.to_csv('paipaiwang1.csv'.format('test'),encoding='utf-8-sig',index=False)

"""
for i in range(len(list_name))
    shortName = getData(i+1,"shortName")
    netChange = driver.find_element(By.XPATH,'((//div[@class="privateOpt"]//div[@class="privateContent"])['+str(i+1)+']//div[@class="newNetFont ppw-green"])[1]').text
    newNet = getData(i+1,"newNet")
    date = driver.find_element(By.XPATH,'((//div[@class="privateOpt"]//div[@class="privateContent"])['+str(i+1)+']//div[@class="newNetTime"])[1]').text
"""