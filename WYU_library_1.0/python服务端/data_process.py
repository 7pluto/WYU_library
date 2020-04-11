from selenium import webdriver
import requests
from PIL import Image
import cv2 as cv
import numpy
import pytesseract
from io import BytesIO
import time
from selenium.webdriver.common.keys import Keys


class Data_process:
    url_frist = 'http://202.192.240.212:82'

    def __init__(self, data):
        #实例化是调用，返回接收客户端的数据
        self.data = data
        #开启浏览器，后面路径是安装谷歌辅助工具，谷歌浏览器才能正常开启
        self.browser=webdriver.Chrome()
        
    def isElementExist(self,element):
            flag=True
            try:
                self.browser.find_element_by_id(element)
                return flag
            except:
                flag=False
                return flag

    def imgToText(self, headers1):
        #获取验证码，find_element_by_id 找html中id属性
        jpg=self.browser.find_element_by_id('ccodeimg')
        img_src=jpg.get_attribute("src")

        #拿到验证码储存
        response =requests.get(img_src,headers=headers1)
        image = Image.open(BytesIO(response.content))
        image.save('D:\\WYU_library.png')

        src = cv.imread('D:\\WYU_library.png')
        #cv.imshow("src", src)
        img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(img,220,255,cv.THRESH_BINARY)
        #cv.imshow("c",binary)
        kernel = numpy.ones((1, 1), numpy.uint8)
        #img = cv.dilate(binary, kernel, iterations=1)
        img = cv.erode(binary, kernel, iterations=1)
        #cv.imshow('open_out', img)
        text = pytesseract.image_to_string(img)
        #cv.waitKey(1)
        print("This OK:%s"%text)
        return text


    def menu(self,dataPro):
        print("\n欢迎使用五邑大学图书馆辅助脚本！")
        print(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        while True:
            print("\n====== ★功能菜单★ ======\n")
            print("0、当前借阅情况  输入：0")
            print("1、借书历史查询  输入：1")
            print("2、目录检索      输入：2")
            print("3、热门借阅      输入：3")
            print("4、退出脚本      输入：4")
            gnxz=input("\n[WYU]等待输入:")
            if gnxz=='0':
                dataPro.dqjy()
            if gnxz=='1':
                list5 = dataPro.lscx(dataPro)
                print("list5:",len(list5))
            if gnxz=='2':
                dataPro.mljs()
            if gnxz=='3':
                dataPro.rmjy()
            if gnxz=='4':
                dataPro.browser.quit()
                break
            def dqjy(self):
                pass
    
    #历史记录
    def lscx(self,dataPro):
        url1 = Data_process.url_frist + '/user/bookborrowedhistory.aspx'
        self.browser.get(url1)
        time.sleep(1)

        print("\n查询中，请销后...\n")

        #从页面中获取信息
        list2,list3 = [],[]
        while True:
            list1 = []
            #find_elements_by_tag_name 找html中的tag属性，<td>..</td>
            tds = self.browser.find_elements_by_tag_name("td")
            for td in tds:
                #.text是里面的本文内容，即显示在网页中的文字
                list1.append(td.text)
            list3 = list3 + list1[5:]
            if(dataPro.isElementExist("ctl00_cpRight_Pagination2_nexthl2")):
                self.browser.find_element_by_id("ctl00_cpRight_Pagination2_nexthl2").click()
            else:
                break

        #切割获取头列表 
        list2 = list1[0:4]

        #删除多余项，有一行数据是空的
        while '' in list3:
            list3.remove('')
        
        #转成二维列表，便于输出
        m,k=0,0
        list4 = []
        list4.append([])
        #list[k++[m++]]
        for i in list3:
            #每四个元素就增加[]
            if m == 4:
                list4.append([])
                k = k + 1
                m=0

            list4[k].append(i)
            list4[k].append('\n')
            m = m + 1
        '''
        for i in range(len(list4)):
            for j in range(len(list4[i])):
                print(list4[i][j])
            print("\n")
        '''
        #关闭浏览器
        self.browser.close()
        return list4

    def mljs(self):
        pass

    def rmjy(self):
        pass


    #登录函数
    def login(self,dataPro):
        url = Data_process.url_frist + '/login.aspx'
        #发送链接到浏览器
        self.browser.get(url)
        #等待，防止页面没有加载完成
        time.sleep(1)

        #获取cookie，没有的话，网站无法识别身份，验证码不匹配
        cookie_bro = self.browser.get_cookies()
        #print(cookie_bro)
        cookie1 = cookie_bro[0]['value']
        #print("当前cookie: "+cookie1)

        headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=' + cookie1,
            'Host': '202.192.240.212:82',
            'Referer': 'http://www.wyu.edu.cn/lib/tb.htm',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Chrome/79.0.3945.88'
        }


        #输入登录信息
        self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtUsername_Lib").send_keys(self.data[:10])
        self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtUsername_Lib").send_keys(Keys.TAB)
        self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtPas_Lib").send_keys(self.data[10:])

        code = dataPro.imgToText(headers1)
        #可以做验证码自动识别
        #code = input("[*]请输入验证码：")
        self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtCode").send_keys(code)
        self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_btnLogin_Lib").click()

        while(dataPro.isElementExist("ctl00_ContentPlaceHolder1_lblErr_Lib")):
            print('验证码识别失败，正在重新识别')
            self.browser.get(url)
            time.sleep(1)
            self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtUsername_Lib").send_keys(self.data[:10])
            self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtUsername_Lib").send_keys(Keys.TAB)
            self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtPas_Lib").send_keys(self.data[10:])

            code = dataPro.imgToText(headers1)
            self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtCode").send_keys(code)
            self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_btnLogin_Lib").click()

        print("\n====== ★登陆成功★ ======\n")
'''
data = '3118001162cwh13671461740'
dataPro = Data_process(data)
dataPro.login(dataPro)
'''