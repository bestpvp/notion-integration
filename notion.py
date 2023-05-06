'''
Author: bestpvp bestpvp@sina.com
Date: 2023-05-03 09:15:26
LastEditors: bestpvp bestpvp@sina.com
LastEditTime: 2023-05-06 15:59:03
FilePath: /notion-intergration/notion.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import json
from notion_client import Client
from notion_client.helpers import get_id

# NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_TOKEN = "secret_8u7AIe1LfhJSmuC9w2fjyUDwrCsj1oZ71hr8mKrk0vt"

while NOTION_TOKEN == "":
    print("NOTION_TOKEN not found.")
    NOTION_TOKEN = input("Enter your integration token: ").strip()

# Initialize the client
notion = Client(auth=NOTION_TOKEN)


def manual_inputs(parent_id="", db_name="") -> tuple:
    """
    Get values from user input
    """
    if parent_id == "":
        is_page_ok = False
        while not is_page_ok:
            input_text = input("\nEnter the parent page ID or URL: ").strip()
            # Checking if the page exists
            try:
                if input_text[:4] == "http":
                    parent_id = get_id(input_text)
                    print(f"\nThe ID of the target page is: {parent_id}")
                else:
                    parent_id = input_text
                notion.pages.retrieve(parent_id)
                is_page_ok = True
                print("Page found")
            except Exception as e:
                print(e)
                continue
    while db_name == "":
        db_name = input("\n\nName of the database that you want to create: ")

    return (parent_id, db_name)


def create_database(parent_id: str, db_name: str) -> dict:
    """
    parent_id(str): ID of the parent page
    db_name(str): Title of the database
    """
    print(f"\n\nCreate database '{db_name}' in page {parent_id}...")
    properties = {
        "Name": {"title": {}},  # This is a required property
        "Description": {"rich_text": {}},
        "In stock": {"checkbox": {}},
        "Food group": {
            "select": {
                "options": [
                    {"name": "🥦 Vegetable", "color": "green"},
                    {"name": "🍎 Fruit", "color": "red"},
                    {"name": "💪 Protein", "color": "yellow"},
                ]
            }
        },
        "Price": {"number": {"format": "dollar"}},
        "Last ordered": {"date": {}},
        "Store availability": {
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {"name": "Duc Loi Market", "color": "blue"},
                    {"name": "Rainbow Grocery", "color": "gray"},
                    {"name": "Nijiya Market", "color": "purple"},
                    {"name": "Gus's Community Market", "color": "yellow"},
                ]
            },
        },
        "+1": {"people": {}},
        "Photo": {"files": {}},
    }
    title = [{"type": "text", "text": {"content": db_name}}]
    icon = {"type": "emoji", "emoji": "🎉"}
    parent = {"type": "page_id", "page_id": parent_id}
    return notion.databases.create(
        parent=parent, title=title, properties=properties, icon=icon
    )


def query_database(database_id: str) -> dict:
    """
    parent_id(str): ID of the parent page
    db_name(str): Title of the database
    """
    return notion.databases.query(
        database_id=database_id
    )


def update_database(database_id: str) -> dict:
    data = {
        "title": [
            {
                "text": {
                    "content": "Today'''s grocery list"
                }
            }
        ],
        "description": [
            {
                "text": {
                    "content": "Grocery list for just kale 🥬"
                }
            }
        ],
        "properties": {
            "Name": {
                "type": "title",
                "title":
                    {
                        "type": "text",
                        "text": {
                            "content": "Can I create a URL property",
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "Can I create a URL property",
                        "href": None
                    }
            },
            "Photo": {
                "url": {}
            },
            "Store availability": {
                "multi_select": {
                    "options": [
                        {
                            "name": "Duc Loi Market"
                        },
                        {
                            "name": "Rainbow Grocery"
                        },
                        {
                            "name": "Gus'''s Community Market"
                        },
                        {
                            "name": "The Good Life Grocery",
                            "color": "orange"
                        }
                    ]
                }
            }
        }
    }
    
    return notion.databases.update(
        database_id=database_id, 
        properties=data['properties'],
        title=data['title']
    )

if __name__ == "__main__":

    # parent_id, db_name = manual_inputs()
    # newdb = create_database(parent_id=parent_id, db_name=db_name)
    # print(f"\n\nDatabase {db_name} created at {newdb['url']}\n")
    # data = query_database('52b8cbf8657743b697e00aee4ee149d1')
    data = update_database('52b8cbf8657743b697e00aee4ee149d1')
    print(json.dumps(data, ensure_ascii=False))
