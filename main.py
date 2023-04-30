'''
Author: bestpvp bestpvp@sina.com
Date: 2023-04-29 19:15:01
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-04-30 16:56:34
FilePath: /notion-intergration/main.py
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


    def get_html(self, url:str, is_get_method: bool = True):
        """
        此函数向指定的URL发送GET或POST请求, 并返回响应的HTML内容。
        :param url: 要发送请求的URL。
        :param is_get_method: 一个布尔值, 指示是否使用GET或POST方法。默认为True(GET)。
        :return: 响应的HTML内容。
        """
        if is_get_method:
            # 发送GET请求
            r = self.session.get(url, headers=self.headers)
        else:
            # 发送POST请求
            r = self.session.post(url, headers=self.headers)
        # 返回响应的HTML内容
        return r.html

    def get_data_by_xpath(self, url:str, xpath:str, is_get_method:bool=True):
        # 获取HTML内容
        html = self.get_html(url, is_get_method)
        # 通过xpath获取元素列表
        xpath_list = html.xpath(xpath)
        # 存储结果的列表
        result = []
        # 遍历元素列表
        for list in xpath_list:
            # 获取元素的title和src属性
            title = list.attrs['alt']
            image = list.attrs['src']
            # 将结果添加到结果列表中
            result.append({
                'title': title,
                'image': image
            })
        # 返回结果列表
        return result

    
    def get_data_by_css(self, url:str, css_selector:str, is_get_method:bool=True):
        # 获取HTML内容
        html = self.get_html(url, is_get_method)
        # 通过CSS选择器获取元素列表
        css_list = html.find(css_selector)
        # 存储结果的列表
        result = []
        # 遍历元素列表
        for list in css_list:
            # 将元素的文本内容添加到结果列表中
            result.append({
                'desc': list.text
            })
        # 返回结果列表
        return result



if __name__ == '__main__':
    
    demo = Spider()
    
    # 使用xpath获取电影海报
    data1 = demo.get_data_by_xpath(url='https://movie.douban.com/top250?start=25&filter=', xpath='//div[@class="pic"]/a/img')
    # 使用CSS选择器获取电影描述
    data2 = demo.get_data_by_css(url='https://movie.douban.com/top250?start=25&filter=', css_selector='.quote .inq')

    # 将获取到的数据合并为一个列表
    result_list = [
        {"title": item1["title"], "image": item1["image"], "desc": item2["desc"]}
        for item1, item2 in zip(data1, data2)
    ]
    
    # 打印结果
    pprint(result_list)

