#- * - coding:utf-8 - * -
import xlrd
import matplotlib.pyplot as plt
import matplotlib
import sys
import threading

matplotlib.rcParams['font.sans-serif'] = ['SimHei']#1
matplotlib.rcParams['font.family']='sans-serif'#2
#解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False#3
'''
1,2,3部分是为了，在生成图片时可以显示中文

'''

reload(sys)#4
sys.setdefaultencoding( "utf-8" )#5
'''
4,5部分设置utf-8编码
'''

#这个是电影的主要类型
labels = [
    u'犯罪',
    u'剧情',
    u'动作',
    u'爱情',
    u'喜剧',
    u'动画',
    u'悬疑',
    u'惊悚',
    u'科幻',
    u'冒险',
    u'家庭',
    u'奇幻',
    u'其他',
    ]#13

#other中的类型占全部类型的少部分，所以设定为其他分类
other = [
    u'历史',
    u'纪录片',
    u'同性',
    u'传记',
    u'运动',
    u'武侠',
    u'古装',
    u'音乐',
    u'儿童'
]
yearandValue = {}#存放年份和次数的键值对

Valuelist = []#存放类型对应的出现次数
for i in xrange(13):#Valuelist初始化
    Valuelist.append(0)



class generatePicture:#生成图片的类
    def __init__(self,fname):
        self.__book__ = xlrd.open_workbook(fname)#读取excel文件实例化
        self.table = self.__book__.sheets()[0]#获取读取第一个sheet内容的句柄
        self.run()
    def run(self):
        self.generateScatter_plots()#画饼状图
        threading.Thread(target=self.generatePie()).start()# 画散点图 线程作图，增加效率


    def generatePie(self):
        '''
        生成饼状图函数
        typer存放获取xls文件中第6列中所以的数据
        '''
        typer = self.table.col_values(5)

        for line in typer:
            '''
            遍历判断这些电影的类型，将出现的次数放入Valuelist中的对应位置
            '''
            for i,j in enumerate(labels):
                if j in line:
                    Valuelist[i] += 1
            for o in other:
                if o in line:
                    Valuelist[12]+=1

        self.Pie(labels,Valuelist)


    def generateScatter_plots(self):
        '''
        生成散点图函数
        '''
        x = []
        y = []
        yearlist = self.table.col_values(3)

        for line  in yearlist:

            if line in yearandValue.keys():
                yearandValue[line] += 1
            elif line != u'年份' :
                yearandValue[line] = 1

        for i in yearandValue:
            x.append(int(i))
            y.append(yearandValue[i])

        self.Scatter(x,y)

    @staticmethod#类中静态函数的装上去
    def Scatter(x,y):#做散点图
        plt.figure()
        plt.title(u'电影按时间的分布的散点图')
        plt.plot(x,y,'ro',color = 'k',marker = '.')
        plt.savefig("ScatterPicture.jpg")
        plt.close()

    @staticmethod#类中静态函数的装上去
    def Pie(labels,Valuelist):#作饼状图
        plt.figure()
        plt.pie(Valuelist,labels=labels,autopct='%1.2f%%') #画饼图（数据，数据对应的标签，百分数保留两位小数点）
        plt.title(u"top250的电影中类型的分布的饼状图")
        plt.savefig("PiePicture.jpg")#保存图片
        plt.close()

if __name__ == '__main__':
    fname = 'data.xls'#excel文件的相对路径

    generatePicture(fname)


    '''
    该程序主要导入的库：xlrd、 matplotlib.pyplot、threading
        1、xlrd是读取xls文件的库
            xlrd.open_workbook(fname)#打开文件
            sheets()[0]#返回对应表的句柄
            .col_values(5)#获取对应行的data
        2、matplotlib.pyplot是画图的库
            pyplot as plt
            plt.figure()#画图入口
            plt.title()#图片标题
            plt.plot(x,y,'ro',color = 'k',marker = '.')#作散点图
            plt.pie（）#做饼状图
            plt.savefig("ScatterPicture.jpg")#存储图
            plt.close()#关闭
            plt.show()#显示图
        3、threading是使用线程的库
            主要作用是多线程画图，增加效率



    '''



    