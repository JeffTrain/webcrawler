from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from PIL import Image
import time
import re
# 首次发布页面
def onerelease(url):
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
    brower = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=yes'])
    brower.get(url)
    # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
    brower.maximize_window()
    # 项目名称
    name = brower.find_element_by_id('ctl00_ContentPlaceHolder1_zbxxV2011_lblgcmc').text
    # 资质要求
    # qualifications=brower.find_element_by_id('ctl00_ContentPlaceHolder1_zbxxV2011_lblzzyq').find_element_by_tag_name('td').text
    # 限价
    fixed_price=brower.find_element_by_id('ctl00_ContentPlaceHolder1_zbxxV2011_InfoGctz1_Label8').text
    fixed_price=float(fixed_price)
    # 信用评分
    credit_score=brower.find_element_by_id('ctl00_ContentPlaceHolder1_zbxxV2011_lblbz').text
    zz1=re.compile('信用评分(≥.*?)分')
    zz2=re.compile('参加投标的单位信用分值(.*?)。')
    zz3=re.compile('参加投标的单位信用分值(.*?)，')
    zz4=re.compile('信用评价体系计分，(.*?)；')
    credit_score1 = re.findall(zz1,credit_score)
    if len(credit_score1)==0:
        credit_score2=re.findall(zz2,credit_score)
        if len(credit_score2)==0:
            credit_score3=re.findall(zz3,credit_score)
            if len(credit_score3)==0:
                credit_score4=re.findall(zz4,credit_score)
                if len(credit_score4)==0:
                    credit_score = '无要求'
                else:
                    credit_score = credit_score4[0]
            else:
                credit_score=credit_score3[0]
        else:
            credit_score=credit_score2[0]
    else:
        credit_score=credit_score1[0]
    one_list=[fixed_price,credit_score]
    time.sleep(1)
    print('正在打开'+str(name)+'网页并保存图片')
    brower.save_screenshot(str(name)+'公开招标信息表'+'.png')
    print('图片保存完成正在关闭网页')
    time.sleep(1)
    brower.close()

    im = Image.open(str(name)+'公开招标信息表'+'.png')
    k, h = im.size  # 图片的宽度和高度
    p = Image.new('RGBA', im.size, (255, 255, 255))  # 使用白色来填充背景
    p.paste(im, (0, 0, k, h), im)
    p.save(str(name)+'公开招标信息表'+'.png')
    im = Image.open(str(name)+'公开招标信息表'+'.png')
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：
    （距离图片左边界距离x，
    距离图片上边界距离y，
    距离图片左边界距离+裁剪框宽度x+w，
    距离图片上边界距离+裁剪框高度y+h）
    '''
    x, y, w = 290, 0, 1080
    region = im.crop((x, y, w, h))
    region.save(str(name)+'公开招标信息表'+'.png')
    return one_list
