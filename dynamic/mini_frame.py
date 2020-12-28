import re
from pymysql import connect

"""
修改后字典
URL_FUNC_DICT = {
    "/index.html": index,
    "/center.html": center
}
"""

URL_FUNC_DICT = dict()


def route(url):
    def set_func(func):
        # URL_FUNC_DICT["/index.py"] = index
        URL_FUNC_DICT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@route("/index.html")     # 相当于 @set_func #  index = set_func(index)
def index():
    with open("./templates/index.html", encoding="utf-8") as f:  # windows上默认编码是gbk，python处理时需要以utf-8方式打开，否则会出错
        content = f.read()

    # content = re.sub(r"\{%content%\}", my_stock_info, content)
    # 创建Connection连接
    conn = connect(host='localhost', port=3306, user='fancy', password='sf825874', database='my_stock', charset='utf8')
    cs = conn.cursor()
    cs.execute("select * from info;")
    my_stock_info = cs.fetchall()

    cs.close()
    conn.close()

    content = re.sub(r"\{%content%\}", str(my_stock_info), content)

    return content


@route("/center.html")
def center():
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这是你从mysql查询来的数据。。。"
    content = re.sub(r"\{%content%\}", my_stock_info, content)  # 替换模板中含 {%content%}  中的数据 为my_stock_info

    return content


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; Charset=utf-8')])
    file_name = env['PATH_INFO']

    """
    if file_name == "/index.py":
        return index()
    elif file_name == "/center.py":
        return center()
    else:
        return 'Hello World! '
    """

    try:
        # func = URL_FUNC_DICT[file_name]
        # return func
        return URL_FUNC_DICT[file_name]()
    except Exception as ret:
        return "产生了异常： %s" % str(ret)


