'''
Author: bestpvp bestpvp@sina.com
Date: 2023-04-29 19:15:01
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-05-06 15:13:55
FilePath: /notion-intergration/douban_spider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from requests_html import HTMLSession, HTML
from pprint import pprint

class Spider:

    def __init__(self):
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0'
        }
        # 创建HTMLSession对象
        self.session = HTMLSession()

    def get_html(self, url:str, is_get_method: bool = True, is_render: bool = False):
        """
        此函数向指定的URL发送GET或POST请求, 并返回响应的HTML内容。
        :param url: 要发送请求的URL。
        :param is_get_method: 一个布尔值, 指示是否使用GET或POST方法。默认为True(GET)。
        :param is_render: 一个布尔值, 指示是否使用loadjs方法。默认为False。
        :return: 响应的HTML内容。
        """
        if is_get_method:
            # 发送GET请求
            r = self.session.get(url, headers=self.headers)
        else:
            # 发送POST请求
            r = self.session.post(url, headers=self.headers)
        if is_render:
            # 返回 loadjs 的 HTML 内容
            r.html.render()
        # pprint(r.html)
        return r.html

class Demo:
    
    @classmethod
    def main(cls):
        """
        此函数为程序的入口点，用于获取电影海报和描述信息，并将结果打印出来。
        """
        douban = Spider()
    
        # 使用xpath获取电影海报
        data1 = douban.get_data_by_xpath(url='https://movie.douban.com/top250?start=25&filter=', xpath='//div[@class="pic"]/a/img')
        # 使用CSS选择器获取电影描述
        data2 = douban.get_data_by_css(url='https://movie.douban.com/top250?start=25&filter=', css_selector='.quote .inq')

        # 将获取到的数据合并为一个列表
        result_list = [
            {"title": item1["title"], "image": item1["image"], "desc": item2["desc"]}
            for item1, item2 in zip(data1, data2)
        ]
        
        # 打印结果
        pprint(result_list)

        return result_list



if __name__ == '__main__':
    
    spider_demo = Spider()
    url = 'https://m.ly.com/scenery_1/list/?cityId=53&cityName=%E5%8C%97%E4%BA%AC&spm=34.44968.44971.0&refid=&from='
    result_html = spider_demo.get_html(url=url, is_render=True)
    xpath_selector = '//div[@class="name"]'
    my_list = result_html.xpath(xpath_selector)
    for i in my_list:

        # # 使用 css
        # if len(i.find('span')) > 0:
        #     print('name: ', i.find('span')[0].text)
        #     if len(i.find('em')) > 0:
        #         print('grade: ', i.find('em')[0].text)
        #     else:
        #         print('grade: N/A')
        #     print('------')

        # 使用 xpath
        if len(i.xpath('//span')) > 0:
            print('name: ', i.xpath('//span')[0].text)
            if len(i.xpath('//em')) > 0:
                print('grade: ', i.xpath('//em')[0].text)
            else:
                print('grade: N/A')
            print('------')
        