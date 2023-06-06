"""
Author: bestpvp bestpvp@sina.com
Date: 2023-04-29 19:15:01
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-06-06 15:02:01
FilePath: /notion-intergration/douban_parser.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import json
from requests_html import HTMLSession


class Douban_parser:
    def __init__(self):
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"
        }
        # 创建HTMLSession对象
        self.session = HTMLSession()

    def get_html(self, url: str, is_render: bool = False) -> object:
        """
        此函数向指定的URL发送GET或POST请求, 并返回响应的HTML内容。
        :param url: 要发送请求的URL。
        :param is_render: 一个布尔值, 指示是否使用loadjs方法。默认为False。
        :return: 响应的HTML内容。
        """
        # 发送GET请求
        r = self.session.get(url, headers=self.headers)
        if is_render:
            # 返回 loadjs 的 HTML 内容
            r.html.render()
        return r.html

    def get_data(self, xpath_dict: dict, resp_html: object) -> dict:
        try:
            result = {}
            for key, value in xpath_dict.items():
                temp = resp_html.xpath(value["xpath"])
                # print("==========", value, temp)
                if len(temp) > 0:
                    if value["tag"] == "text":
                        temp = temp[0].text if temp[0].text else ""
                    elif value["tag"] == "int":
                        temp = int(temp[0].text) if temp[0].text else int(0)
                    elif value["tag"] == "float":
                        temp = float(temp[0].text) if temp[0].text else float(0)
                    elif value["tag"] == "blank":
                        temp = temp[0].strip()
                    else:
                        temp = (
                            temp[0].attrs[value["tag"]]
                            if temp[0].attrs[value["tag"]]
                            else ""
                        )
                    result[key] = temp
        except Exception as e:
            print(
                e.__traceback__.tb_frame.f_globals["__file__"].split("/")[-1],
                e.__traceback__.tb_lineno,
                e,
            )
            return {}
        else:
            return result

    def book_parser(self, url: str, is_render: bool = False) -> dict:
        try:
            resp_html = self.get_html(url=url, is_render=is_render)
            xpath_dict = {
                "name": {"xpath": "/html/body/div[3]/h1/span", "tag": "text"},
                "cover": {"xpath": '//*[@id="mainpic"]/a/img', "tag": "src"},
                "author": {"xpath": '//*[@id="info"]/span[1]/a', "tag": "text"},
                "rating_num": {
                    "xpath": '//*[@id="interest_sectl"]/div/div[2]/strong',
                    "tag": "float",
                },
            }
            data = self.get_data(xpath_dict=xpath_dict, resp_html=resp_html)
            data["douban_url"] = url
        except Exception as e:
            result = {
                "code": -1,
                "data": "{}({}) 异常: {}".format(
                    e.__traceback__.tb_frame.f_globals["__file__"].split("/")[-1],
                    e.__traceback__.tb_lineno,
                    e,
                ),
            }
        else:
            result = {"code": 0, "data": data}
        # print(json.dumps(result, ensure_ascii=False))
        return result

    def movie_parser(self, url: str, is_render: bool = False) -> dict:
        try:
            resp_html = self.get_html(url=url, is_render=is_render)
            xpath_dict = {
                "name": {"xpath": '//*[@id="content"]/h1/span[1]', "tag": "text"},
                "cover": {"xpath": '//*[@id="mainpic"]/a/img', "tag": "src"},
                "desc": {
                    "xpath": '//*[@id="link-report-intra"]/span',
                    "tag": "text",
                },
                "country": {
                    "xpath": '//*[@id="info"]/text()[preceding-sibling::span[text()="制片国家/地区:"]]',
                    "tag": "blank",
                },
                "author": {"xpath": '//*[@id="info"]/span[1]/span[2]/a', "tag": "text"},
                "rating_num": {
                    "xpath": '//*[@id="interest_sectl"]/div[1]/div[2]/strong',
                    "tag": "float",
                },
            }
            data = self.get_data(xpath_dict=xpath_dict, resp_html=resp_html)
            data["douban_url"] = url
        except Exception as e:
            result = {
                "code": -1,
                "data": "{}({}) 异常: {}".format(
                    e.__traceback__.tb_frame.f_globals["__file__"].split("/")[-1],
                    e.__traceback__.tb_lineno,
                    e,
                ),
            }
        else:
            result = {"code": 0, "data": data}
        # print(json.dumps(result, ensure_ascii=False))
        return result


if __name__ == "__main__":
    demo = Douban_parser()
    # demo.book_parser(url='https://book.douban.com/subject/36291252')
    demo.movie_parser(url="https://movie.douban.com/subject/35587790/")
