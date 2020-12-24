import re


def index():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "hahaha 这是你本月名称。。。"
    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content


def center():
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这是你从mysql查询来的数据。。。"
    content = re.sub(r"\{%content%\}", my_stock_info, content)  # 替换模板中含 {%content%}  中的数据 为my_stock_info

    return content


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; Charset=utf-8')])
    file_name = env['PATH_INFO']

    if file_name == "/index.py":
        return index()
    elif file_name == "/center.py":
        return center()
    else:
        return 'Hello World! '
