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
def index(ret):
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

    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>    
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvalue="%s">
        </td>  
        </tr>
    """

    html = ""
    for line_info in my_stock_info:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6], line_info[7], line_info[1])

    # content = re.sub(r"\{%content%\}", str(my_stock_info), content)
    content = re.sub(r"\{%content%\}", html, content)

    return content


@route("/center.html")
def center(ret):
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    # 1 建立连接
    conn = connect(host='localhost', port=3306, user='fancy', password='sf825874', database='my_stock', charset='utf8')
    # 2 获取游标
    cs = conn.cursor()
    # 3 数据查询
    cs.execute("select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id;")    # 查询连结数据表后的结果
    my_stock_info = cs.fetchall()
    # 4 关闭游标和连接
    cs.close()
    conn.close()

    # 5 组合html格式数据
    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>    
        <td>%s</td>
        <td>
            <a type=""button class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"> </span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemidvalue="300268">
        </td>  
        </tr>
    """

    html = ""
    for line_info in my_stock_info:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6])

    content = re.sub(r"\{%content%\}", html, content)  # 替换模板中含 {%content%}  中的数据 为my_stock_info

    return content


@route(r"/add/(\d+)\.html")     # 注意，此处的（\d+）将股票代码对应的页面数字作为一个分组，没有这步处理，下面的查询、插入等操作会无法进行
def add_focus(ret):
    # 1. 获取股票代码
    stock_code = ret.group(1)
    print(ret.group(1))

    # 2. 判断是否有这个股票代码
    conn = connect(host='localhost', port=3306, user='fancy', password='sf825874', database='my_stock', charset='utf8')
    cs = conn.cursor()
    sql = """select * from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    # 如果没有这个股票代码，就认为这个使非法请求
    if not cs.fetchone():
        cs.close()
        conn.close()
        return "没有这只股票！"

    # 3. 判断以下是否已经关注过
    sql = """ select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    # 如果查出来了，那么表示已经关注过
    if cs.fetchone():
        cs.close()
        conn.close()
        return "已经关注过了，请勿重复关注！"

    # 4. 添加关注
    sql = """insert into focus (info_id) select id from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    conn.commit()
    cs.close()
    conn.close()

    return "关注成功 ...."


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; Charset=utf-8')])
    file_name = env['PATH_INFO']

    try:
        # func = URL_FUNC_DICT[file_name]
        # return func
        # return URL_FUNC_DICT[file_name]()
        for url, func in URL_FUNC_DICT.items():     # url对应key  func对应value，存储在字典URL_FUNC_DICT中
            ret = re.match(url, file_name)
            if ret:
                return func(ret)                # 此处返回请求的url在URL_FUNC_DICT中的value值，对匹配后的值交给对应路由函数
        else:
            return "请求的url(%s)没有对应的函数..." % file_name

    except Exception as ret:
        return "产生了异常： %s" % str(ret)


