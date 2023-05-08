<!--
 * @Author: bestpvp bestpvp@sina.com
 * @Date: 2023-04-29 20:46:33
 * @LastEditors: bestpvp bestpvp@sina.com
 * @LastEditTime: 2023-05-08 17:53:56
 * @FilePath: /notion-intergration/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# notion-integration

notion-integration：基于 requests_html 和 notion http api，实现了豆瓣的图书、电影、电视信息同步到 notion 数据库的功能。

### 功能特性

- 结构清晰，功能明确
- 使用同步功能，代码编写逻辑更自然

### 快速开始

1. 安装依赖
    
    ```bash
    pip install -r requirements.txt
    ```
    
    *系统要求：Python 版本在 3.5.2 及以上*
    
2. 获取豆瓣链接
    
    ```bash
    图书：https://book.douban.com/subject/36350632/
    电影：https://movie.douban.com/subject/35209731/
    电视：https://movie.douban.com/subject/1427318/
    ```
    
3. 申请 notion integration：[My integrations | Notion Developers](https://www.notion.so/my-integrations)
    
    ```bash
    NOTION_API_TOKEN = "secret_your_api_token"
    ```
    
4. 创建 notion database
    
    *注意点：创建的 database 需要添加集成的权限（Add connections），找到你的应用*
    
    ```bash
    BOOK_DATABASE_ID = "your_database_id"
    MOVIE_DATABASE_ID = "your_database_id"
    TV_DATABASE_ID = "your_database_id"
    ```
    
5. 运行 [main.py](http://main.py) 后，查看结果
    
    ```bash
    python ./main.py
    ```