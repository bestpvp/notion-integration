"""
Author: bestpvp bestpvp@sina.com
Date: 2023-05-08 14:52:36
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-06-06 15:20:08
FilePath: /notion-intergration/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import sys
import json
import conf
from douban_parser import Douban_parser
import notion_api


def main(douban_url: str = conf.DOUBAN_URL):
    # 判断douban_url里是否包含 movie 或 book的关键字
    if "movie" in douban_url:
        notion_db = conf.MOVIE_DATABASE_ID
        db_type = "movie"
    elif "book" in douban_url:
        notion_db = conf.BOOK_DATABASE_ID
        db_type = "book"
    else:
        print("2. 链接错误,请检查链接")
        sys.exit(1)
    print(f"2. 豆瓣类型: {db_type}, notion 数据库 id: {notion_db}")

    # 根据 db_type 判断获取 douban 的信息
    douban = Douban_parser()
    if db_type == "book":
        data = douban.book_parser(douban_url)
    elif db_type == "movie":
        data = douban.movie_parser(douban_url)
    else:
        print("3. 链接错误,请检查链接")
        sys.exit(1)
    print(f"3. 从 豆瓣 获取的数据报文: {json.dumps(data, indent=4, ensure_ascii=False)}")

    # 如果数据成功获取, 则更新notion数据库
    if data["code"] == 0:
        # 根据db_type, 生成不同的notion_body
        if db_type == "book":
            notion_body = {
                "parent": {"type": "database_id", "database_id": notion_db},
                "properties": {
                    "书名": {
                        "title": [
                            {"type": "text", "text": {"content": data["data"]["name"]}}
                        ]
                    },
                    "书籍分类": {"multi_select": []},
                    "豆瓣评分": {"number": data["data"]["rating_num"]},
                    "豆瓣链接": {"url": data["data"]["douban_url"]},
                    "封面": {
                        "files": [
                            {
                                "type": "external",
                                "name": f"{data['data']['name']}.jpg",
                                "external": {"url": data["data"]["cover"]},
                            }
                        ]
                    },
                    "状态": {"select": {"name": "想读"}},
                    "作者": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": data["data"]["author"]},
                            }
                        ]
                    },
                },
            }
        elif db_type == "movie":
            notion_body = {
                "parent": {
                    "type": "database_id",
                    "database_id": notion_db,
                },
                "properties": {
                    "影片名": {
                        "title": [
                            {"type": "text", "text": {"content": data["data"]["name"]}}
                        ]
                    },
                    "影片类型": {"multi_select": []},
                    "豆瓣评分": {"number": data["data"]["rating_num"]},
                    "影片链接": {"url": data["data"]["douban_url"]},
                    "封面": {
                        "files": [
                            {
                                "type": "external",
                                "name": f"{data['data']['name']}.jpg",
                                "external": {"url": data["data"]["cover"]},
                            }
                        ]
                    },
                    "状态": {"select": {"name": "想看"}},
                    "国家": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": data["data"]["country"]},
                            }
                        ]
                    },
                    "剧情简介": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": data["data"]["desc"]},
                            }
                        ]
                    },
                    "导演": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": data["data"]["author"]},
                            }
                        ]
                    },
                },
            }
        else:
            print("链接错误,请检查链接")
            sys.exit(1)

        # 更新notion数据库
        return notion_api.update_notion_database(notion_body)
    else:
        print(f"3. 从 豆瓣 获取失败, 错误信息: {data['msg']}")
        return False


if __name__ == "__main__":
    if len(sys.argv) == 1:
        url = input("1. 请输入豆瓣链接: ")
    else:
        url = sys.argv[1]
    main(douban_url=url)
