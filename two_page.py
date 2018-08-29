from selenium import webdriver
from first_page import one_page
import time
import os
def twopage(url):
    brower = webdriver.Chrome()  # 打开浏览器
    brower.get(url)
    main_window = brower.current_window_handle
    zhaobiao=brower.find_element_by_id('ddlZblx').find_elements_by_tag_name('option')[3].click()
    login=brower.find_element_by_id('Button1').click()
    time.sleep(3)
    tr = brower.find_elements_by_tag_name('tbody')[2].find_elements_by_tag_name('tr')
    today = tr[1].find_elements_by_tag_name('td')[1].text
    print('正在处理第二页数据')
    two_page = brower.find_elements_by_tag_name('tbody')[-1].find_elements_by_tag_name('td')[1].click()
    time.sleep(3)
    # 获得最后一个窗口的句柄
    brower.switch_to.window(brower.window_handles[0])
    tr = brower.find_elements_by_tag_name('tbody')[2].find_elements_by_tag_name('tr')
    today2 = tr[1].find_elements_by_tag_name('td')[1].text
    datalis=[]
    if today2 != today:
        print('第二页无数据')
        brower.close()
        return datalis
    else:
        for index in range(1, len(tr) - 1):
            # 将每行的第一个单元格文字保存起来
            table = brower.find_element_by_class_name('main').find_element_by_id('gvList')  # 获取表格
            current_tr = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[index]  # 猎取表格的第I行
            td1 = current_tr.find_elements_by_tag_name('td')[0].text
            print('正在下载%s的数据' % td1)
            # 将每行的第二个单元格文字保存起来
            td2 = current_tr.find_elements_by_tag_name('td')[1].text
            if today != td2:
                print('第二页数据收集完成！')
                brower.close()
                time.sleep(3)
                break
            # print(td1,td2)

            # 点击表格中每一个a连接
            current_tr.find_elements_by_tag_name('td')[0].find_element_by_tag_name("a").click()
            time.sleep(2)
            # 获得最后一个窗口的句柄
            brower.switch_to.window(brower.window_handles[-1])

            # 获得url地址
            url = brower.current_url
            lis = one_page(url)
            liss = tuple(lis)
            datalis.append(liss)

            brower.close()
            # 获取完地址，窗口切换回到主窗口
            windows = brower.window_handles
            for window in windows:
                if window == main_window:
                    brower.switch_to.window(main_window)
        return datalis

