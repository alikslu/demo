from selenium import  webdriver
import requests
from bs4 import BeautifulSoup
import re
import time
# import multiprocessing


class Tools:
    removeImg = re.compile('<img.*?>')
    removBr = re.compile('<br>')
    removeHef = re.compile('<a href.*?>')
    removeA = re.compile('</a>')
    removeClass = re.compile('<a class.*?>|<aclass.*?>')
    removeNull = re.compile(' ')

    def remove(self, te):
        te = re.sub(self.removeImg, '', te)
        te = re.sub(self.removBr, '\n', te)
        te = re.sub(self.removeHef, '', te)
        te = re.sub(self.removeA, '', te)
        te = re.sub(self.removeClass, '', te)
        te = re.sub(self.removeNull, '', te)
        return te

textTools = Tools()
# diver=webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])


def getHTMLText(url):
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""

def get_target_url(url, url_list):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('a', attrs={"class": "j_th_tit"})

    for li in liTags:
        test = '情缘' in li["title"]
        if test:

            test2 ='月' in li["title"]
            if test2:
                a = "http://tieba.baidu.com/" + li["href"]
                print(li["title"])
                url_list.append(a)

def writeText(titleText, fpath):
    try:
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(str(titleText) + '\n')
            f.write('\n')
            f.close()
    except:
        return ""

def writeUnivlist(lis, li, timelis, namelis,fpath, num,titleText):

    with open(fpath, 'a', encoding='utf-8') as f:
        print(num)
        print(li)
        for i in range(num):
            f.write(str(namelis[i])+'     '+li[i]+'   ')
            f.write('http://tieba.baidu.com/home/main?un='+str(namelis[i])+ '\n')
            f.write(str(lis[i]) + '\n')
            f.write(str(timelis[i]) + '\n')
            f.write('*' * 50)
            f.write(str(titleText))
            f.write('*' * 50)
        f.close()

# def printTitle(url):
#     try:
#
#         diver.get(url)
#         html = diver.page_source
#         soup = BeautifulSoup(html, "html.parser")
#         titleTag = soup.find_all('title')
#         patten = re.compile(r'<title>(.*?)</title>', re.S)
#         get_max_page = soup.find("a",text='尾页').attrs['href']
#         title = re.findall(patten, str(titleTag))
#         pattern = re.compile(r'(.*\d*[?pn=])(\d*)')
#         maxpage=int(pattern.match(get_max_page).group(2))
#         if maxpage>5:
#             return title, maxpage
#     except:
#         return ""
#
#
# def fillUnivlist(lis, li, html):
#     try:
#         patten = re.compile(r'<div id="post_content_\d*" class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
#         nbaInfo = re.findall(patten, str(html))
#         pattenFloor = re.compile(r'<span class="tail-info">(\d*楼)</span><span class="tail-info">', re.S)
#         floorText = re.findall(pattenFloor, str(html))
#         number = len(nbaInfo)
#         for i in range(number):
#             Info = textTools.remove(nbaInfo[i])
#             Info1 = textTools.remove(floorText[i])
#             lis.append(Info1)
#             li.append(Info)
#     except:
#         return ""



# if __name__=="__main__":
#     url_list = []
#     urls=[]
#     tieba_names=['唯满侠']
#     for tieba_name in tieba_names:
#         urls.append('https://tieba.baidu.com/f?kw='+tieba_name+'&ie=utf-8')
#     print(urls)
#     output_file = 'StockInfo.txt'
#     for i in urls:
#         target_url = get_target_url(i, url_list)
#         print(url_list)
#     for url in url_list:
#         count = 0
#         print('done')
#         print('doing--'+url)
#         html = getHTMLText(url)
#         try:
#             titleText, Maxpage = printTitle(html)
#             writeText(titleText, output_file)
#             print('正在爬取%s' % (titleText))
#             print('一共有%s页等待爬取' % (Maxpage))
#             for i in range(Maxpage):
#                 i = i + 1
#                 lis = []
#                 li = []
#                 html = getHTMLText(url + '?pn=' + str(i))
#                 fillUnivlist(lis, li, html)
#                 writeUnivlist(lis, li, output_file, len(lis))
#                 count = count + 1
#                 print(r'在爬取第%s 页' % i, end="")
#                 time.sleep(0.1)
#         except:
#             print('fail'+url)
# main()

def printTitle(html):
    try:

        soup = BeautifulSoup(html, "html.parser")
        titleTag = soup.find_all('title')
        patten = re.compile(r'<title>(.*?)</title>', re.S)
        title = re.findall(patten, str(titleTag))
        return title
    except:
        return ""


def fillUnivlist(lis, li, timelis, namelis, html):



        patten = re.compile(r'<div id="post_content_\d*" class="d_post_content j_d_post_content " style="display:;">(.*?)</div>', re.S)
        nbaInfo = re.findall(patten, str(html))
        #爬取内容

        pattenFloor = re.compile(r'<span class="tail-info">(\d*楼)</span><span class="tail-info">', re.S)
        floorText = re.findall(pattenFloor, str(html))
        # 爬取楼层

        timeFloor=re.compile(r'<span class="tail-info">(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', re.S)
        timeText =re.findall(timeFloor, str(html))
        # 爬取时间


        nameFloor = re.compile(r'&quot;un&quot;:&quot;(.*?)&quot;,&quot;id&quot', re.S)
        nameText = re.findall(nameFloor, str(html))
        nameText = eval(repr(nameText).replace('\\\\', '\\'))
        # 爬取作者
        #print(nbaInfo)
        # print(str(html))
        number = len(nbaInfo)
        print('crabwing done'+str(number))
        try:
            for i in range(number):

                Info = textTools.remove(nbaInfo[i])

                if len(Info)>5:
                    if "post_bubble_top" not in Info:
                        print('quilitity aquire')

                        lis.append(Info)
                        li.append(floorText[i])
                        timelis.append(timeText[i])
                        namelis.append(nameText[i])

            return floorText[1]
        except:
            pass


if __name__=="__main__":
    url_list = ['https://tieba.baidu.com/p/5965555042','https://tieba.baidu.com/p/5965554953','https://tieba.baidu.com/p/5969489615']
    urls=[]
    tieba_names=['双梦镇','乾坤一掷','圣墓山','纵月六只鹅','念破']
    # tieba_names=['唯满侠','风雨大姨妈']
    for tieba_name in tieba_names:
        urls.append('https://tieba.baidu.com/f?kw=' + tieba_name + '&ie=utf-8')
        urls.append('https://tieba.baidu.com/f?kw='+tieba_name+'&ie=utf-8&pn=50')
        urls.append('https://tieba.baidu.com/f?kw=' + tieba_name + '-&ie=utf-8&pn=100')
        urls.append('https://tieba.baidu.com/f?kw=' + tieba_name + '&ie=utf-8&pn=150')
        urls.append('https://tieba.baidu.com/f?kw=' + tieba_name + '&ie=utf-8&pn=200')

    output_file = 'qiny.txt'
    for i in urls:
        print('开始寻找帖子')
        print('*'*50)
        target_url = get_target_url(i, url_list)
        print('"帖子名字:'+i)
        print('*' * 50)
    # print(url_list)
    url_list=list(set(url_list))
    for url in url_list:
        # url='https://tieba.baidu.com/p/5971279381'

        count = 0
        print('done')
        print('在爬取的链接为--'+url)
        html = getHTMLText(url)
        titleText = printTitle(html)


        print('正在爬取的标题为%s' % (titleText))


        a=0

        li = []
        lis = []
        namelis = []
        timelis = []

        for i in range(1000):
            i = i + 1
            html = getHTMLText(url + '?pn=' + str(i))
            b=fillUnivlist(lis, li,timelis ,namelis,html)
            print(r'在爬取第%s 页' % i)
            print(a)
            print(b)
            try:
                if b!=a:
                    a=b
                else:

                    break
                print('----')
                # print(a)
                # print(li)
                # print(lis)
                # print(timelis)

                count = count + 1
                time.sleep(0.1)
                if count>5:
                # writeText(titleText, output_file)
                # print(titleText)
                # print('okkkkkk')
                # print(lis)
                # print(timelis)
                # print(len(lis))


                    writeUnivlist(lis, li, timelis, namelis, output_file, len(lis),titleText)

                else:
                    print('页数不足5页')
            except:
                pass



