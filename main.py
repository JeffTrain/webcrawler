#!/usr/bin/env python
# -*- coding: utf-8 -*-
from one_page import onepage
from two_page import twopage
from openpyxl import Workbook
import time
print('程序将在5秒后启动，过程大约6—8分钟。')
print('友情提示：请尽量不要操作计算机，等待程序运行完成')
time.sleep(5)
url='http://www.ciac.sh.cn/XmZtbbaWeb/Gsqk/GsFbList.aspx'
list1,today=onepage(url)
list2=twopage(url)
list=list1+list2
print('正在保存数据到EXCEL中')
time.sleep(3)
class saveExcelData(object):
    def __init__(self,dataList,sheetTitle,fileName):
        self.dataList = dataList
        self.sheetTitle = sheetTitle
        self.fileName = fileName
    def savaData(self):
        # 1.实例化对象
        workbook = Workbook()
        # 2. 激活一个工作表
        sheet = workbook.active
        # 3. 给表定个标题 title
        sheet.title = self.sheetTitle
        # 4. 通过sheet.append（）按行添加数据
        for i in self.dataList:
                sheet.append(i)
        workbook.save(self.fileName)

zz=saveExcelData(list,'sheet1',str(today)+'.xlsx')
#第一个对参数是列表 保存多少行取决于列表中元组个数 ，每行保存多少列取决于元组中的元素个数
zz.savaData()
print('数据保存完成，程序将在5秒后运行结束。')
time.sleep(5)
exit()