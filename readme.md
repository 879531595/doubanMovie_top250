#爬取豆瓣电影top 250
###环境：widows、python2.7、threading、urllib2、xlwt、re、BeautifulSoup 

###需求：
（网址：https://movie.douban.com/top250）爬取每部电影的排名、名字、导演、上映年份、国家、影片类型、评分、评价人数、及下面的小短评

###分析：
	进入网站发现每页显示25部电影 一共10页
	
![](https://i.imgur.com/ho3u47B.png)
	
###1、编辑函数获取一页中每部电影具体内容的的url。
	def put_Data_to_queue(url):
    try:
        html = urllib2.urlopen(url).read()
    except Exception,e:
        print e
        print 'html open error'
    content_queue.put(html)

	将其存储至准备好的队列content_queue中


###2、再使用threading包编写多线程函数，获取250部电影的所有url
	for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='\
				.format(i*25)
        threading.Thread(target=put_Data_to_queue,\
		args=(url,)).start()


###3、class PqThred(threading.Thread):#继承并重写threading.Thread类，实现其可以既可以获取队列数据，又能进行多线程执行。（具体实现见源代码）



	'''
    本项目导入的包有：BeautifulSoup、urllib2、re、Queue、
	threading、os、sys、xlwt、time。
    核心库：
            1、urllib2：向webServer发送请求，获取网站上html的
			内容
            2、BeautifulSoup：可以根据html中的标签准确的获取相
			应位置的内容
            3、re：使用正则表达式，获取特位置的data
            4、Queue、threading：本项目将queue结合threaing，
			继承Thread.threading重写了一个新的类，在
			Thread.threading的基础向写入了queue属性，以及
			writeData方法，保证了采集数据的安全。大大的提高了采
			集和写入的效率
            5、xlwt:将数据写入excel的库
    辅助库：
        	1、os：报错时及时关闭程序，对文件的删除操作
        	2、sys：涉及到编码的问题
        	3、time:起延时作用







	'''