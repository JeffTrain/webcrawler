from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from PIL import Image
import time
from detailed_information import detailed_information
from one_release import onerelease
import os
import re
# 第二页
def one_page(url):
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
    # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
    brower.get(url)
    main_window = brower.current_window_handle
    #项目名称
    name = brower.find_element_by_id('Label6').text
    os.makedirs(str(name))
    os.chdir(str(name))
    # 招标方式
    tendering=brower.find_element_by_id('lblzbfs').text
    # 报建编号
    report_number = brower.find_element_by_id('lblbjbh').text
    # 地区替换
    zz = re.compile('\D{2}')
    list = re.findall(zz, report_number)[-1]
    dict = {'HP': '黄浦', 'XH': '徐汇', 'CN': '长宁', 'JA': '静安', 'PT': '普陀',
            'HK': '虹口', 'YP': '杨浦', 'MH': '闵行', 'BS': '宝山', 'JD': '嘉定',
            'PD': '浦东', 'JS': '金山', 'SJ': '松江', 'QP': '青浦', 'FX': '奉贤',
            'KQ': '跨区', 'LG': '临港', 'NH': '南汇', 'ZB': '闸北', 'CM': '崇明'}
    region=dict[list]
    url = brower.current_url
    if len(url) > 58:
        # 合理最低价
        lowest_price = brower.find_element_by_id('Label12').text
        # 下浮比率
        floating_rate = brower.find_element_by_id('Label13').text
    else:
        lowest_price='无数据'
        floating_rate='无数据'
    # 第一中标人
    first_per=brower.find_elements_by_tag_name('tbody')[1].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[0].text.strip()
    #第一中标人价格
    offer=brower.find_elements_by_tag_name('tbody')[1].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[-1].text.strip()
    offer=float(offer)  #把价格变成浮点数
    # 参加投标总人数
    total_number=brower.find_elements_by_tag_name('tbody')[1].find_elements_by_tag_name('tr')[-1].find_element_by_tag_name('span').text
    # 暂列金额
    provisional_sum=brower.find_element_by_id('lblzlje').text
    if len(provisional_sum)==0:
        provisional_sum=0
    # 暂估价
    valuation=brower.find_element_by_id('lblzgj').text
    # 其中专业工程暂估价
    # engineering_evaluation=brower.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[-6].find_elements_by_tag_name('span')[3].text
    # 公示期限
    time_limit=brower.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[-4].find_elements_by_tag_name('td')[-1].text

    first_release=brower.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[-5]
    first_release.find_elements_by_tag_name('td')[-1].find_element_by_tag_name("a").click()
    # 获得最后一个窗口的句柄
    brower.switch_to.window(brower.window_handles[-1])
    # 获得url地址
    first_release_url = brower.current_url
    #获取内页的函数返回值
    if tendering == '公开招标':
        one_list = onerelease(first_release_url)
        # 提取出内页函数返回的第一个值
        fixed_price = one_list[0]
        # 提取内页函数返回的第二个值
        credit_score = one_list[1]
    else:
        # 设置邀请招标限价为中标总价
        fixed_price = offer
        # 提取内页函数返回的第三个值
        credit_score = '该项目为邀请招标，限价默认为中标价'
    # 获取完地址，窗口切换回到主窗口
    windows = brower.window_handles
    time.sleep(2)
    for window in windows:
        if window == main_window:
            brower.switch_to.window(main_window)
    detailed=brower.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[-2]
    detailed.find_elements_by_tag_name('td')[-1].find_element_by_tag_name("a").click()
    # 获得最后一个窗口的句柄
    brower.switch_to.window(brower.window_handles[-1])
    # 获得url地址
    detailed_url = brower.current_url
    waste_standard=detailed_information(detailed_url)
    os.replace('temp.png',str(name) + '中标候选人公示详细信息'+'.png')
    windows = brower.window_handles # 获取完地址，窗口切换回到主窗口
    time.sleep(2)
    for window in windows:
        if window == main_window:
            brower.switch_to.window(main_window)

    brower.maximize_window()
    time.sleep(1)
    print('正在打开'+str(name)+'网页并保存图片')
    brower.save_screenshot(str(name) + '中标候选人公示'+'.png')
    print('图片保存完成正在关闭网页')
    time.sleep(1)

    # 暂列金额
    provisional_sum = int(provisional_sum) + int(valuation)
    # 不扣暂定下浮=100*（1-中标总价/限价）
    no_provisional = 100 * (1-(offer/fixed_price))
    no_provisional=round(no_provisional,2)
    # 暂定下浮=100*（1 -（中标总价 - 暂列金额） / （限价 - 暂列金额））
    suspension=100*(1-(offer-provisional_sum)/(fixed_price-provisional_sum))
    suspension=round(suspension,2)
    # 报价下浮=1-（限价/中标总价）
    quotation_floated=1-(fixed_price/offer)
    quotation_floated=round(quotation_floated,4)
    # 设置评估方法
    if fixed_price >2000:
        evaluation_method='综合评估法'
    else:
        evaluation_method='简单比价法'
    first_list = [region,name,fixed_price,lowest_price,floating_rate,first_per,offer,
                  provisional_sum,total_number,waste_standard,time_limit,str(no_provisional)+'%',
                  str(suspension)+'%',credit_score,evaluation_method,str(quotation_floated)+'%']
    # print(first_list)
    brower.close()


    im = Image.open(str(name) + '中标候选人公示'+'.png')
    k, h = im.size  # 图片的宽度和高度
    p = Image.new('RGBA', im.size, (255, 255, 255))  # 使用白色来填充背景
    p.paste(im, (0, 0, k, h), im)
    p.save(str(name) + '中标候选人公示'+'.png')
    im = Image.open(str(name) + '中标候选人公示'+'.png')
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
    region.save(str(name) + '中标候选人公示'+'.png')
    os.chdir('../')
    return first_list
