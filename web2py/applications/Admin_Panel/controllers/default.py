# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from urlparse import urlparse
import json
import urllib
import gluon

def parse_url(url):
    o = urlparse(url)
    return str(o[2][1:]).split('/')

def check_user():
    if auth.user != None:
        return True
    else:
        return False


def check_admin():
    if check_user():
        user_permission = db.executesql("SELECT permission FROM user_permissions WHERE user_id='" + str(auth.user.id) + "'")
        if user_permission:
            if user_permission[0][0] == "admin":
                return True
            else:
                return False
    else:
        return False

def index():
    #x = db.executesql("select * from ")
    gtp = get_top_products('20140501', '20170611', 10)
    gtpp = XML(gtp)
    stp = top_suppliers('20140501', '20170611', 10)
    stpp = XML(stp)

    profit_revenue = get_profit()


    return dict(gtpp = gtpp, stpp=stpp, profit_revenue= profit_revenue)

def load_tags():
    pid = request.vars.pid
    query = "exec dbo.tag_proc "+pid
    tag_data = db.executesql(query, as_dict=True);
    return json.dumps(tag_data, ensure_ascii=False)

def load_all_tags():
    query = "select tag_name from tag;"
    all_tag_data = db.executesql(query, as_dict=True);
    return json.dumps(all_tag_data, ensure_ascii=False)

def new_tag_save():
    pid = request.vars.pid
    tags = request.vars.tags
    list = []
    tags = tags.split(',')
    for tag in tags:
        list.append( tag.split(' = ') )

    for item in list:
        tag_name = str(item[0].strip())
        status = str(item[1])
        tag_name = tag_name.strip()
        status = status.strip()
        query = "select tag_id from tag where tag_name = '" + tag_name + "';"
        tag_id = db.executesql(query, as_dict=True)
        print('tag= ')
        print(tag_id)
        tag_id = tag_id[0]['tag_id']
        tag_id = str(tag_id)
        print (tag_name,status)
        result = db.executesql("select * from tag_association where tag_id = '" + tag_id + "' and product_id = '"+pid+"';", as_dict=True)
        if(status == 'true'):
            if(len(result) == 0):
                query = 'insert into tag_association (tag_id,product_id) values (' + str(tag_id) + ',' + str(pid) + ')'
                db.executesql(query)
        if(status == 'false'):
            if(len(result) == 1):
                query = 'delete from tag_association where tag_id = '+tag_id
                db.executesql(query)

def add_product():
    supplier_association_id = request.vars.id
    query = "insert into inventory select * from product where " \
            "product_id in (select product_id from get_product where supplier_association_id = " + supplier_association_id + ")"
    db.executesql(query)
    return json.dumps( dict(response=1) )

def set_normalize():
    supplier_id = request.vars.supplier_id
    dest = request.vars.dest
    source = request.vars.source
    sql = 'insert into product ' + source + ' select ' + dest + ' from supplier_' + supplier_id
    print sql

def load_supplier_data():
    supplier_id = request.vars.id
    supplier_fields = db.executesql("SELECT COLUMN_NAME FROM devora.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'supplier_"+supplier_id+"'", as_dict=True)
    return json.dumps(supplier_fields, ensure_ascii=False)

def tag_save():
    tag = request.vars.tag
    query = "insert into tag (tag_name) values ('"+tag+"')"
    db.executesql(query)
    response_code = 1
    return dict(response_code=response_code)

def save_default_image():
    pid = request.vars.pid
    img_id = request.vars.img_id
    query = "update image set [default] = '1' where product_id = " + pid
    print(query)
    db.executesql(query)

def normalization():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    suppliers = db.executesql('select * from supplier', as_dict=True)
    return dict(location=T('Admin Panel - normalization'), suppliers=suppliers)

def tag():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    products = db.executesql('select * from product', as_dict=True)
    return dict(location=T('Admin Panel - Tag Manager'), products=products)

def load_image():
    pid = request.vars.pid
    images = db.executesql('select * from image where product_id = '+pid, as_dict=True)
    return json.dumps(images, ensure_ascii=False)

def image():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    image = db.executesql('select * from product', as_dict=True)
    return dict(location=T('Admin Panel - Image Manager'), images=image)

def products():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    test = db.executesql('select * from get_product', as_dict=True)
    return dict(location=T('Admin Panel - Products'),test=test)

def edit_product():
    supplier_association_id = request.vars.id
    title = request.vars.title
    desc = request.vars.desc
    query = "update get_product set title = '" + title + "', description = '" + desc + "' where supplier_association_id = '" + supplier_association_id + "'"

    db.executesql(query)

    products = db.executesql("SELECT * FROM get_product")
    user_data = db.executesql("SELECT * FROM auth_user")
    suppliers = db.executesql("SELECT * FROM supplier")

    return dict(location=T('Admin Panel - Index'), suppliers=suppliers, user_data=user_data, products=products)

def staff():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
    if request.args(0) == 'edit':
        edited = db.executesql("UPDATE user_permissions SET permission='" + request.vars.permission + "' WHERE user_id='" + str(request.vars.user_id) + "'")
        staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
        redirect('staff')

    return dict(location=T('Admin Panel - Staff'), staff=staff)

def chart_bars():
    meses_chart="['Candy', 'Bread', 'Milk', 'Coffee']" #Change this dynamically
    dados_chart="[3.5, 4, 5, 2]" #Change this dynamically
    title="Online-Retail-Admin"
    stitle="Products` Report"
    dados_map={}
    dados_map["dados"]=dados_chart
    dados_map["meses"]=meses_chart
    dados_map['titulo']=title
    dados_map['subtitulo']=stitle

    chart="""

        Highcharts.setOptions({
            lang:{
            downloadJPEG: "Download em imagem JPG",
            downloadPDF: "Download em documento PDF",
            downloadPNG: "Download em imagem PNG",
            downloadSVG: "Download em vetor SVG",
            loading: "Lendo...",
            noData: "Sem dados para mostrar",
            printChart: "Imprimir Gráfico",
            }
            });

                // Build the chart
                $('#chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: '%(titulo)s'
            },
            subtitle: {
                text: '%(subtitulo)s'
            },
            xAxis: {
                categories: %(meses)s,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Money($)'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>R$ {point.y:.1f} </b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            credits:{enabled:false},
            series: [{
                name: 'Products',
                data: %(dados)s

            }]
        });

       """ %dados_map
    return dict(chart=XML('<script>'+chart+'</script>'))

def stats():
    return dict(location=T('Admin Panel - Stats'))

def supplier():
    suppliers = db.executesql("SELECT * FROM supplier", as_dict=True)
    print "inside supplier()"
    if request.args(0) == 'add':
        api_key = "132sdfas5475"
        api_address = "http://sup3.com/api"
        added = db.executesql("INSERT INTO supplier (supplier_name, status, contact_first, contact_last, contact_phone, contact_email, api_key, api_address) VALUES ('"+request.vars.supplier_name+"', '"+request.vars.status+"', '"+request.vars.contact_first+"', '"+request.vars.contact_last+"', '"+request.vars.contact_phone+"', '"+request.vars.contact_email+"', '"+api_key+"', '"+api_address+"')")
        redirect('default/supplier')
    elif request.args(0) == 'edit':
        api_key = "132sdfas5485"
        api_address = "http://sup3.com/api"
        edited = db.executesql("UPDATE supplier SET supplier_name='"+request.vars.supplier_name+"', status='"+request.vars.status+"', contact_first='"+request.vars.contact_first+"', contact_last='"+request.vars.contact_last+"', contact_phone='"+request.vars.contact_phone+"', contact_email='"+request.vars.contact_email+"', api_key='"+"a4d45a5f6"+"', api_address='"+"http://www.google.com"+"' WHERE supplier_id='"+request.vars.supplier_id+"'")
        suppliers = db.executesql("SELECT * FROM supplier", as_dict=True)
        redirect('default/supplier')
    elif request.args(0) == 'delete':
        deleted = db.executesql("DELETE FROM supplier WHERE supplier_id='"+request.vars.id+"'")
        suppliers = db.executesql("SELECT * FROM supplier", as_dict=True)
        redirect('default/supplier')
    return dict(location=T('Admin Panel - Suppliers'), suppliers=suppliers)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def stats():
    (meses_chart, dados_chart) = splittter()
    title = "Online-Retail-Admin"
    stitle = "Report by dates"
    dados_map = {}
    dados_map["dados"] = dados_chart
    dados_map["meses"] = meses_chart
    dados_map['titulo'] = title
    dados_map['subtitulo'] = stitle

    container = """
                // Build the chart
                $('#container').highcharts({

            title: {
                text: '%(titulo)s',
                x: -20
            },
            subtitle: {
                text: '%(subtitulo)s',
                x: -20
            },
            xAxis: {
                categories: %(meses)s,

            },
            yAxis: {
                title: {
                    text: 'Money($)'
                },
                plotLines: [{
                	value: 0,
                	width: 1,
                	color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: '$'
            },
            series: [{
            	name: 'Dates',
            	data: %(dados)s
            	}]
        });

       """ % dados_map
    return dict(chart=XML('<script>' + container + '</script>'))


def splittter():
    test = get_profit_by_date("WEEK", -10)
    date_list = []
    amount_list = []
    for item in test:

        date_list.append("'" +item['sale_week']+"'")
        amount_list.append(str(item['total_sales']))
    date_list = ", ".join(date_list)
    date_list = "[" + date_list + "]"

    amount_list = ", ".join(amount_list)
    amount_list = "[" + amount_list + "]"
    print date_list
    print amount_list
    return (date_list, amount_list)

"""
DATABASE RETREIVAL FUNCTIONS
"""
#Tested and working!
def get_top_products(begin, end, limit):
    limitby = 10
    if limit != None:
        limitby = limit
    top_product = db.executesql("SELECT TOP " + str(limitby) + " product.title, count(*) as num_sales FROM order_item LEFT JOIN purchase_order ON order_item.purchase_order_no = purchase_order.purchase_order_no left join product on product.product_id = order_item.product_id WHERE purchase_order.sale_date > '20141102' AND purchase_order.sale_date < '20171104' AND title is not null GROUP BY product.title ORDER BY num_sales desc")

    print top_product
    top_product = [["Name", "Top Products"]] + top_product
    print str(json.dumps(top_product)).replace('\"', ' \' ')
    top_product = replace_double_quote(json.dumps(top_product))
    #top_product = [['Name', 'Top Products']] + top_product
    return top_product

#Not tested
def get_sales_by_location(begin, end, limit):
    limitby = 10
    if limit != None:
        limitby = limit

    """
    sales_location = db.executesql("(SELECT guest.state, count(order_item.order_item_id) as sales"\
                                    "FROM order_item"\
                                    "LEFT JOIN purchase_order ON order_item.purchase_order_no = purchase_order.purchase_order_no"\
                                    "LEFT JOIN guest ON purchase_order.guest_id = guest.guest_id"\
                                    "WHERE purchase_order.sale_date > '" + begin + "' AND purchase_order.sale_date < '"+end+"' GROUP BY guest.state)")
    """
    sales_location = db.executesql("SELECT supplier_name,  FROM supplier", as_dict=True)
    return json.dumps(sales_location)


#TO IMPLEMENT
def top_suppliers(begin, end, limit):
    limitby = 10
    if limit != None:
        limitby = limit

    top_supplier = db.executesql("select top 10 supplier_name, count(*) as sale_count from supplier inner join order_item on supplier.supplier_id = order_item.supplier_id inner join purchase_order on order_item.purchase_order_no = purchase_order.purchase_order_no where purchase_order.sale_date > '20051104' and purchase_order.sale_date < '20171104'group by supplier_name order by sale_count desc")
    top_supplier = [["Name", "Top Suppliers"]] + top_supplier
    top_supplier = replace_double_quote(json.dumps(top_supplier))
    return top_supplier

def amount_by_suppllier(begin, end, limit):
    limitby = 10
    if limit != None:
        limitby = limit

    top_products = db.executesql()
    return json.dumps(top_products)

def get_profit(): #scope = day/month/year
    profit = db.executesql("select sum(round(order_item.sale_price - order_item.sale_cost, 2)) as profit, sum(round(order_item.sale_price,2)) as revenue from order_item inner join purchase_order on order_item.purchase_order_no = purchase_order.purchase_order_no where purchase_order.sale_date between '20051104' and '20171104'")
    return profit

def get_profit_by_date(time, amount):
    timely_profit = db.executesql("select cast(dateadd(WEEK, datediff(week, 0, sale_date),0) as date) as sale_week, round(cast(sum(order_item.sale_price - order_item.sale_cost) as float),2,2) as total_sales from purchase_order inner join order_item on order_item.purchase_order_no = purchase_order.purchase_order_no where sale_date between dateadd(WEEK, -10, getdate()) and getdate()  group by dateadd(WEEK, datediff(week, 0, sale_date),0)", as_dict=True)
    print  timely_profit
    # for i in range(0,len(timely_profit)):
    #     timely_profit[i][1] = int(timely_profit[i][1])
    #timely_profit = replace_double_quote(timely_profit)
    return timely_profit


def supplier_compare(supplier1, supplier2):
    return 0

def replace_double_quote(strs):
    strs = str(strs).replace('\"', '\'')
    return strs