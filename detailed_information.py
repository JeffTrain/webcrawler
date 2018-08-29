from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from PIL import Image
import time

def detailed_information(url):
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
    # name = brower.find_element_by_id('ctl00_ContentPlaceHolder1_zbxxV2011_lblgcmc').text
    # waste_standard 废标情况
    tr=brower.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
    if len(tr)==4:
        td=tr[2].find_elements_by_tag_name('td')
        if len(td)==1:
            waste_standard=tr[2].find_element_by_tag_name('td').text
        else:
            waste_standard=tr[2].find_element_by_tag_name('td').text
    else:
        waste_standard = tr[-2].find_element_by_tag_name('td').text
    brower.maximize_window()
    time.sleep(1)
    print('正在打开招标公示页面并保存图片')
    brower.save_screenshot('temp.png')
    print('图片保存完成正在关闭网页')
    time.sleep(1)
    brower.close()

    im = Image.open('temp.png')
    k, h = im.size  # 图片的宽度和高度
    p = Image.new('RGBA', im.size, (255, 255, 255))  # 使用白色来填充背景
    p.paste(im, (0, 0, k, h), im)
    p.save('temp.png')
    im = Image.open('temp.png')
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
    region.save('temp.png')
    return waste_standard