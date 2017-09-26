#- * - coding:utf-8 - * -
from Queue import Queue
import threading
import urllib2
import re
import os
import sys
import xlwt
import time
from bs4 import BeautifulSoup
'''

Author __Evin__
Emaill 879531595@qq.com

'''

'''
Queue的方法：
1.put（）存放数据
2.set（）取出数据

'''

#----------------------------------------------------------------------------------------------------------------------#
'''
变量实例化部分
'''

reload(sys)
sys.setdefaultencoding( "utf-8" )
urls_queue = Queue()#存放url的queue
content_queue = Queue()#存放html数据的queue
data_queue = Queue()#存放待写入数据
lock  = threading.Lock()#线程锁




RowHeadContent = [
    u'排名',
    u'电影名',
    u'导演',
    u'年份',
    u'国家',
    u'类型',
    u'评分',
    u'评论人数',
    u'描述',

]#excel首行的数据
#----------------------------------------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------------------------------------#
'''
函数定义部分
put_Data_to_queue（url）函数传入url，使用到urllib2库对网站上的html进行抓取将值存入content_queue中便于之后的操作，其中使用了try excpt
防止ip受限制时报错使程序崩溃
ThreadGetData()开十个线程执行put_Data_to_queue（url）函数，来获取所以html中data,lock锁保证数据不紊乱

'''


def ThreadGetData():#多线程操作
    lock.acquire()#锁定
    '''
    总共用250条记录共10页，每个线程获取每一页的内容
    '''
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
        threading.Thread(target=put_Data_to_queue,args=(url,)).start()
    lock.release()#释放
    # threading.Thread(target=excelinit).start()
    print 'html write complete'


#获取url的内容，将其存入queue
def put_Data_to_queue(url):
    try:
        html = urllib2.urlopen(url).read()
    except Exception,e:
        print e
        print 'html open error'
    content_queue.put(html)
#----------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------#
'''
主体类部分：
    继承了threading.Thread类
'''
class PqThred(threading.Thread):#继承threading.Thread类
    DemandContent = []
    def __init__(self,queue):
        threading.Thread.__init__(self)#执行父类的init
        print 'Please wait for program initialization...'
        try:
            '''
            类初始化时删除data.xls。防止写入数据时发生冲突报错
            '''
            os.remove('data.xls')
        except:
            pass
        self.queue = queue
        self.Pqrun()
    def Pqrun(self):
        self.getContent()
        self.writeData()

    #从content_queue获取相应的数据存入data_queue
    def getContent(self):
        for i in xrange(10):#遍历提取content_queue中所有的data
            try:
                html = content_queue.get()
            except Exception,e:
                print e
            #获取
            content = BeautifulSoup(html,"html.parser",from_encoding='utf-8').findAll("div",{"class":"item"})
            for line in content:
                self.DemandContent = []
                star = line.find("div",{"class":"star"}).findAll("span")#获取评分和评价数
                pData = line.find("p").get_text().strip()
                namelist = line.findAll("span",{"class":"title"})#获取电影名称列表
                yearCountryType = pData.split('\n')[1].split('/')

                #提取排名
                ID = line.find("em").get_text()
                self.DemandContent.append(ID)

                #提取子页链接
                link = line.find("a").attrs['href']
                # self.ypshu ,self.dpshu = self.get_url_inside_dat(link)#影评数和短评数
                urls_queue.put([ID,link])#将子页的链接和ID存入urls_queue

                #提取电影名
                #EnglishName =namelist[1].get_text().replace('/','')#英文名
                name = namelist[0].get_text()
                self.DemandContent.append(name)

                #导演
                director = re.findall(ur'\:(.*?)\xa0',pData)[0].strip()
                self.DemandContent.append(director)

                #年份
                year = re.findall('[\d]+',pData)[0]
                # year = yearCountryType[0].strip()
                self.DemandContent.append(year)

                #国家
                country =yearCountryType[1].strip()
                self.DemandContent.append(country)

                #类型
                typer = yearCountryType[2].strip()
                label = typer.split(' ')
                
                self.DemandContent.append(typer)

                #提取电影评分
                grade = star[1].get_text()
                self.DemandContent.append(grade)

                #提取电影评论数
                evaluate =star[3].get_text()
                self.DemandContent.append(evaluate)

                #提取电影描述
                try:
                    '''
                    存在某些电影没有描述
                    '''
                    inq = line.find("span",{"class":"inq"}).get_text()
                except:
                    inq = ''
                self.DemandContent.append(inq)

                print self.DemandContent

                #将self.DemandContent存入data_queue中
                data_queue.put(self.DemandContent)

    #向excel里写数据
    def writeData(self):
        print 'writing....'
        #excel对象实例化
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)

        #文件名
        sheet = book.add_sheet('data', cell_overwrite_ok=True)#实例化对excel操作的句柄sheet

        #写入第一行的数据
        for i in xrange(9):
            sheet.write(0, i,RowHeadContent[i])
        n = data_queue.qsize()#获取data_queue中的长度

        #遍历将数据写入excel
        for i in xrange(n):
            content = data_queue.get()
            for i in xrange(9):
                row = content[0]
                sheet.write(int(row),i,content[i])
                book.save('data.xls')#保存
        print 'write success'
#----------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------#
'''
    main程序入口
'''
if __name__ == '__main__':

    '''
        1、首先调用ThreadGetData()函数，开十个线程对html中的数据读取到content_queue
        2、延时
        3、执行重写的PqThred类，对content_queue中的数据提取、分析、写入

    '''
    ThreadGetData()#1
    time.sleep(1)#2
    PqThred(content_queue).start()#3









'''
    本项目导入的包有：BeautifulSoup、urllib2、re、Queue、threading、os、sys、xlwt、time。
    核心库：
            1、urllib2：向webServer发送请求，获取网站上html的内容
            2、BeautifulSoup：可以根据html中的标签准确的获取相应位置的内容
            3、re：使用正则表达式，获取特位置的data
            4、Queue、threading：本项目将queue结合threaing，继承Thread.threading重写了一个新的类，在Thread.threading的基础向写入
            了queue属性，以及writeData方法，保证了采集数据的安全。大大的提高了采集和写入的效率
            5、xlwt:将数据写入excel的库
    辅助库：
        1、os：报错时及时关闭程序，对文件的删除操作
        2、sys：涉及到编码的问题
        3、time:起延时作用







'''

