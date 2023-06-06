"""
Author: bestpvp bestpvp@sina.com
Date: 2023-05-03 09:15:26
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-06-01 18:08:55
FilePath: /notion-intergration/notion_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import json
from jsonpath import jsonpath
import requests
import conf


def update_notion_database(body: dict) -> dict:
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
            "code": -1,
            "data": "{}({}) 异常: {}".format(
                e.__traceback__.tb_frame.f_globals["__file__"].split("/")[-1],
                e.__traceback__.tb_lineno,
                e,
            ),
        }
    else:
        title = jsonpath(resp_json, expr="$.properties..title[0].text.content")
        msg = f"导入信息成功, 标题信息为: {title}"
        result = {"code": 0, "data": msg}
    print(f"4. 更新 notion: {json.dumps(result, ensure_ascii=False)}")
    return result


if __name__ == "__main__":
    # body = {
    #     "parent": {
    #         "type": "database_id",
    #         "database_id": "20e0857f40de427a85cb58349299ff9f"
    #     },
    #     "properties": {
    #         "书名": {
    #             "title": [
    #                 {
    #                     "type": "text",
    #                     "text": {
    #                         "content": "中国的历史之路"
    #                     }
    #                 }
    #             ]
    #         },
    #         "书籍分类": {
    #             "multi_select": []
    #         },
    #         "豆瓣评分": {
    #             "number": 8.1
    #         },
    #         "豆瓣链接": {
    #             "url": "https://book.douban.com/subject/36291252"
    #         },
    #         "封面": {
    #             "files": [
    #                 {
    #                     "type": "external",
    #                     "name": "s34454856.jpg",
    #                     "external": {
    #                         "url": "https://img9.doubanio.com/view/subject/s/public/s34454856.jpg"
    #                     }
    #                 }
    #             ]
    #         },
    #         "状态": {
    #             "select": {
    #                 "name": "想读"
    #             }
    #         },
    #         "作者": {
    #             "rich_text": [
    #                 {
    #                     "type": "text",
    #                     "text": {
    #                         "content": "[英]伊懋可"
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    # }

    body = {
        "parent": {
            "type": "database_id",
            "database_id": "342b560cffb043f49f11bcc7f9942b74",
        },
        "properties": {
            "影片名": {"title": [{"type": "text", "text": {"content": "movie_name"}}]},
            "影片类型": {"multi_select": []},
            "豆瓣评分": {"number": 7.6},
            "影片链接": {"url": "https://movie.douban.com/subject/35587790"},
            "封面": {
                "files": [
                    {
                        "type": "external",
                        "name": "test.jpg",
                        "external": {
                            "url": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2882458713.jpg"
                        },
                    }
                ]
            },
            "状态": {"select": {"name": "想看"}},
            "国家": {"select": {"name": "movie_country", "color": "purple"}},
            "剧情简介": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "讲述了只在晚上才能看到东西的盲人针灸师偶然目击王世子的死亡，为揭露事实真相而孤军奋战的故事，刘海镇饰演了因丧子之痛而逐渐失去理智的国王，而柳俊烈则饰演了只有在晚上才能看到东西的盲人针灸师。"
                        },
                    }
                ]
            },
        },
    }

    update_notion_database(body)
