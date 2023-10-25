from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas
import time
import re
from lxml import html
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains        # 导入鼠标事件库

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


login()
mouse = driver.find_element(By.XPATH,'//div[@class="comp-header-nav-item fz14"]/div/span[@class="ellipsis"]')
ActionChains(driver).move_to_element(mouse).perform()
driver.find_element(By.XPATH,'//a[@class="comp-header-user-item icon-trade"]').click()
time.sleep(2)

# 解析网页
page = driver.page_source
soup = BeautifulSoup(page,'html.parser')

list_url = []   # 用于保存目标网站
list_name = []  # 用于保存目标名称
url_a = soup.select('div:nth-child(2) > div.shortName > a')    # 找到所爬取的网页
names = soup.select('div> div > div:nth-child(2) > div.shortName > a')  # 找到名称
for u in url_a:
    url = u['href']     # 得到网站
    list_url.append(url)
for name in names:
    list_name.append(name.get_text())

print(list_name)
print(list_url)

# 开始解析每一个基金网页

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

for ind in range(len(list_name)):
  driver.get(list_url[ind])       # 加载网站
  time.sleep(1)
  driver.find_element(By.XPATH,'(//h3[contains(text(),"历史净值")])[1]').click()        # 点击历史净值
  time.sleep(1)
  for i in range(10):
    js = 'document.getElementsByClassName("tbody")[0].scrollTop=100000'
    driver.execute_script(js)
    time.sleep(0.1)  # 防止滑动太快，没有读取到结果

  #以下开始出问题
  page_url = driver.page_source  # 解析当前网页
  htmlEtree = etree.HTML(page_url)
  hideIds = ['z464f7','z4c26f','z4a6ab']
  divList = htmlEtree.xpath('//div[@class="nav-tr comp-common-flex aic"]') #
  #print("divList:")
  #print(divList)
  
  tdDivs = []
  for div in divList:
    nextDivs = div.xpath('./div[@class="nav-td comp-common-flex aic"]')
    for nextDiv in nextDivs:
      if nextDivs.index(nextDiv) == 0:
        continue
      tdDivs.append(nextDiv)
  print("tdDivs: ")
  print(tdDivs)

  resultList = []
  for tdDiv in tdDivs:
    labels = tdDiv.xpath("./*")
    nowResultList = []
    for label in labels:
      classStr = label.xpath("./@class")[0]
      print(classStr)
      if classStr not in hideIds:
        nowResultList.append(label.xpath("./text()")[0])
    resultList.append("".join(nowResultList))

  print(resultList)
  for reslut in resultList:
    print(reslut)
