'''
Author: bestpvp bestpvp@sina.com
Date: 2023-05-03 09:15:26
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-05-08 15:41:47
FilePath: /notion-intergration/notion_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import json
from jsonpath import jsonpath
import requests
import conf

def update_notion_database(body:dict) -> dict:
    """
    更新notion数据库
    body模板:
    {
        "parent": {
            "type": "database_id",
            "database_id": "20e0857f40de427a85cb58349299ff9f"
        },
        "properties": {
            "书名": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "中国的历史之路"
                        }
                    }
                ]
            },
            "书籍分类": {
                "multi_select": []
            },
            "豆瓣评分": {
                "number": 8.1
            },
            "豆瓣链接": {
                "url": "https://book.douban.com/subject/36291252"
            },
            "封面": {
                "files": [
                    {
                        "type": "external",
                        "name": "s34454856.jpg",
                        "external": {
                            "url": "https://img9.doubanio.com/view/subject/s/public/s34454856.jpg"
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
                            "content": "[英]伊懋可"
                        }
                    }
                ]
            }
        }
    }
    """
    try:
        # print(body)
        r = requests.request(
            "POST",
            "https://api.notion.com/v1/pages",
            json=body,
            headers={
                "Authorization": "Bearer " + conf.NOTION_API_TOKEN,
                "Notion-Version": "2022-06-28",
            },
        )
        r.raise_for_status()
        resp_json = r.json()
    except Exception as e:
        result = {
            'code': -1,
            'data': '{}({}) 异常: {}'.format(e.__traceback__.tb_frame.f_globals["__file__"].split("/")[-1], e.__traceback__.tb_lineno, e)
        }
    else:
        title = jsonpath(resp_json, expr='$.properties..title[0].text.content')
        msg = f"导入信息成功, 标题信息为: {title}"
        result = {
            'code': 0,
            'data': msg
        }
    # print(json.dumps(result, ensure_ascii=False))
    return result


if __name__ == "__main__":

    body = {
        "parent": {
            "type": "database_id",
            "database_id": "20e0857f40de427a85cb58349299ff9f"
        },
        "properties": {
            "书名": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "中国的历史之路"
                        }
                    }
                ]
            },
            "书籍分类": {
                "multi_select": []
            },
            "豆瓣评分": {
                "number": 8.1
            },
            "豆瓣链接": {
                "url": "https://book.douban.com/subject/36291252"
            },
            "封面": {
                "files": [
                    {
                        "type": "external",
                        "name": "s34454856.jpg",
                        "external": {
                            "url": "https://img9.doubanio.com/view/subject/s/public/s34454856.jpg"
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
                            "content": "[英]伊懋可"
                        }
                    }
                ]
            }
        }
    }

    update_notion_database(body)

