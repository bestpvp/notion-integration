'''
Author: bestpvp bestpvp@sina.com
Date: 2023-05-08 14:52:36
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-05-08 16:02:21
FilePath: /notion-intergration/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import conf
from douban_parser import Douban_parser
import notion_api

def main(douban_url:str=conf.DOUBAN_BOOK_URL, notion_db:str=conf.BOOK_DATABASE_ID):
    # 实例化
    douban = Douban_parser()
    # 获取 douban 的图书信息
    data = douban.book_parser(douban_url)
    print(data)
    # 如果数据成功获取
    if data['code'] == 0:
        # 构造notion的书籍信息
        notion_book_body = {
            "parent": {
                "type": "database_id",
                "database_id": notion_db
            },
            "properties": {
                "书名": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": data['data']['name']
                            }
                        }
                    ]
                },
                "书籍分类": {
                    "multi_select": []
                },
                "豆瓣评分": {
                    "number": data['data']['rating_num']
                },
                "豆瓣链接": {
                    "url": data['data']['douban_url']
                },
                "封面": {
                    "files": [
                        {
                            "type": "external",
                            "name": "s34454856.jpg",
                            "external": {
                                "url": data['data']['cover']
                            }
                        }
                    ]
                },
                "状态": {
                    "select": {
                        "name": "想读"
                    }
                },
                "作者": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": data['data']['author']
                            }
                        }
                    ]
                }
            }
        }
        # 更新notion数据库
        return notion_api.update_notion_database(notion_book_body)
    else:
        return data

if __name__ == "__main__":
    main()