from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from first_page import one_page
import time
import os

def onepage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Connection': 'Keep - Alive',
        'Accept-Language': 'zh-CN',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Host': 'www.ciac.sh.cn'
    }  # 设置请求头部信息

    cap = DesiredCapabilities.PHANTOMJS.copy()  # 使用copy()防止修改原代码定义dict
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=yes'])
    # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
    driver.get(url)
    zhaobiao=driver.find_element_by_id('ddlZblx').find_elements_by_tag_name('option')[3].click()
    login=driver.find_element_by_id('Button1').click()
    time.sleep(3)

    main_window = driver.current_window_handle
    # table = driver.find_element_by_class_name('main').find_element_by_id('gvList')
    tr = driver.find_elements_by_tag_name('tbody')[2].find_elements_by_tag_name('tr')
    today = tr[1].find_elements_by_tag_name('td')[1].text
    os.makedirs(str(today))
    os.chdir(str(today))

    datalist=[('区县','项目名称','限价','合理最低价','浮率','中标单位','中标总价','不可竞争费',
               '参加单位数量','废标家数','公示日期','不扣暂定下浮','暂定下浮','信用分','评估方法','报价下浮')]
    for index in range(1,len(tr)-1):
        # 将每行的第一个单元格文字保存起来
        table = driver.find_element_by_class_name('main').find_element_by_id('gvList')  #获取表格
        current_tr = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[index] #猎取表格的第I行

        td1 = current_tr.find_elements_by_tag_name('td')[0].text
        print('正在下载%s的数据'%td1)
        # 将每行的第二个单元格文字保存起来
        td2 = current_tr.find_elements_by_tag_name('td')[1].text
        if today!=td2:
            break
        # print(td1,td2)

        # 点击表格中每一个a连接
        current_tr.find_elements_by_tag_name('td')[0].find_element_by_tag_name("a").click()
        time.sleep(2)
        # 获得最后一个窗口的句柄
        driver.switch_to.window(driver.window_handles[-1])

        # 获得url地址
        url = driver.current_url
        lis=one_page(url)
        liss=tuple(lis)
        datalist.append(liss)

        driver.close()
        # 获取完地址，窗口切换回到主窗口
        windows = driver.window_handles
        for window in windows:
            if window == main_window:
                driver.switch_to.window(main_window)
    return datalist,today



