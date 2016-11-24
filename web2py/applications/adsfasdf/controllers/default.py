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
    else:
        return False

def index():

    gtp = get_top_products('20140501', '20170611', 10)
    gtpp = XML(gtp)
    stp = top_suppliers('20140501', '20170611', 10)
    stpp = XML(stp)

    profit_revenue = get_profit()


    return dict(gtpp = gtpp, stpp=stpp, profit_revenue= profit_revenue)

def add_product():
    supplier_association_id = request.vars.id
    query = "insert into inventory select * from product_info where " \
            "product_info_id in (select product_info_id from get_product where supplier_association_id = " + supplier_association_id + ")"
    db.executesql(query)
    response_code = 1
    return response_code

def products():
    if check_user() == False:
        T('Permission Denied')
        redirect('index')

    test = db.executesql('select * from get_product', as_dict=True)
    return dict(location=T('Admin Panel - Products'),test=test)

def edit_product():
    supplier_association_id = request.vars.id
    price = request.vars.price
    cost = request.vars.cost
    title = request.vars.title
    desc = request.vars.desc
    color = request.vars.color.decode('string_escape')
    size = request.vars.size.decode('string_escape')
    supplier_sku = request.vars.supplier_sku.decode('string_escape')
    supplier_name = request.vars.supplier_name.decode('string_escape')
    manufacturer = request.vars.manufacturer.decode('string_escape')
    # query = "update get_product set manufacturer='"+manufacturer+"' ,supplier_name='"+supplier_name+"' ,supplier_sku='"+supplier_sku+"', color_name = '"+color+"', size_name = '"+size+"',description='"+desc+"',title='"+title+"',cost='"+cost+"',price='"+price+"' where supplier_association_id = '" + supplier_association_id+"'"
    query = "update get_product set color_name = '" + color + "', size_name = '" + size + "',price='" + price + \
            "' where supplier_association_id = '" + supplier_association_id + "'"

    db.executesql(query)

    query = "update get_product set manufacturer='" + manufacturer + "',description='" + desc + "',title='" \
        + title + "' where supplier_association_id = '" + supplier_association_id + "'"
    db.executesql(query)

    query = "update get_product set supplier_sku='" \
            + supplier_sku + "',cost='" + cost + \
            "' where supplier_association_id = '" + supplier_association_id + "'"

    db.executesql(query)
    query = "update get_product set supplier_name='" + supplier_name + \
        "' where supplier_association_id = '" + supplier_association_id + "'"
    db.executesql(query)
    # query = "update get_product set supplier_name='" + supplier_name + "' ,supplier_sku='" \
    #     + supplier_sku + "',cost='" + cost + "',price='" + price + \
    #     "' where supplier_association_id = '" + supplier_association_id + "'"
    # db.executesql(query)
    # response_code = 1
    # return dict(response_code=response_code)
    # def db_edit_product(supplier_association_id, edits):
    products = db.executesql("SELECT * FROM get_product")
    user_data = db.executesql("SELECT * FROM auth_user")
    suppliers = db.executesql("SELECT * FROM supplier")

    return dict(location=T('Admin Panel - Index'), suppliers=suppliers, user_data=user_data, products=products)


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


def supplier():
    if check_user() == False:
        redirect('index')

    suppliers = db.executesql("SELECT * FROM supplier", as_dict=True)

    if request.args(0) == 'add':
        api_key = "132sdfas5475"
        api_address = "http://sup3.com/api"
        supplier_name=request.vars.supplier_name.decode('string_escape')
        status=request.vars.status.decode('string_escape')
        contact_first=request.vars.contact_first.decode('string_escape')
        contact_last=request.vars.contact_last.decode('string_escape')
        contact_phone=request.vars.contact_phone.decode('string_escape')
        contact_email=request.vars.contact_email.decode('string_escape')

        added = db.executesql("INSERT INTO supplier (supplier_name, status, contact_first," \
                              " contact_last, contact_phone, contact_email, api_key, api_address)" \
                              " VALUES ('"+supplier_name+"', '"+status+"', '" \
                              +contact_first+"', '"+contact_last+"', '"+contact_phone+"', '"\
                              +contact_email+"', '"+api_key+"', '"+api_address+"')")
        redirect('default/supplier')
    elif request.args(0) == 'edit':
        api_key = "132sdfas5485"
        api_address = "http://sup3.com/api"
        supplier_name = request.vars.supplier_name.decode('string_escape')
        status = request.vars.status.decode('string_escape')
        contact_first = request.vars.contact_first.decode('string_escape')
        contact_last = request.vars.contact_last.decode('string_escape')
        contact_phone = request.vars.contact_phone.decode('string_escape')
        contact_email = request.vars.contact_email.decode('string_escape')
        edited = db.executesql("UPDATE supplier SET supplier_name='"+supplier_name+"', status='"+status+ \
                               "', contact_first='"+contact_first+"', contact_last='"+contact_last+\
                               "', contact_phone='"+contact_phone+"', contact_email='"+contact_email+\
                               "', api_key='"+"a4d45a5f6"+"', api_address='"+"http://www.google.com"+"' WHERE supplier_id='"+request.vars.supplier_id+"'")
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

def staff():
    staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
    if request.args(0) == 'edit':
        edited = db.executesql("UPDATE user_permissions SET permission='" + request.vars.permission + "' WHERE user_id='" + str(request.vars.user_id) + "'")
        staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
        redirect('staff')

    return dict(location=T('Admin Panel - Staff'), staff=staff)

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
