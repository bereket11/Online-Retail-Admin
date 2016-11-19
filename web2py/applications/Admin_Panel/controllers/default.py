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
        if user_permission[0][0] == "admin":
            return True
        else:
            return False
    else:
        return False

def index():
    title = "Dashboard"
    data = XML([
          ['Name', 'Top Suppliers'],
          ['Dell' , 5],
          ['Apple', 7],
          ['Toshiba', 3],
          ['Acer', 2],
          ['Sony', 6],
          ['Panasonic', 1],
        ])
    return dict(data=data, title=title)

def add_product():
    supplier_association_id = request.vars.id
    query = "insert into inventory_info select * from product_info where " \
            "product_info_id in (select product_info_id from get_product where supplier_association_id = " + supplier_association_id + ")"
    db.executesql(query)
    query = "insert into devora.dbo.inventory (product_info_id ,title ,price ,discounted_price ,color_name ,color_code ,color_group ,size_name ,size_order ,length ,width ,height ,unit ,weight ,status) select product_info_id ,title ,price ,discounted_price ,color_name ,color_code ,color_group ,size_name ,size_order ,length ,width ,height ,unit ,weight ,status from product where product_id in (select product_id from get_product where supplier_association_id = " + supplier_association_id + ")"
    db.executesql(query)
    response_code = 1
    return response_code

def products():
    if check_admin() == False:
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


def chart_bars():
    if check_user() == False:
        redirect('index')

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
    if check_user() == False:
        redirect('index')

    test = {'test1':'22', 'test2':'20', 'test3':'9'}
    print json.dumps(test)
    return dict(location=T('Admin Panel - Stats'))

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

def product():
    return dict(location=T('Admin Panel - Inventory'))

def implement():
    return dict(location=T('Admin Panel - Implement'))

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

def staff():
    staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
    if request.args(0) == 'edit':
        edited = db.executesql("UPDATE user_permissions SET permission='" + request.vars.permission + "' WHERE user_id='" + str(request.vars.user_id) + "'")
        staff = db.executesql("SELECT * FROM view_permissions", as_dict=True)
        redirect('staff')

    return dict(location=T('Admin Panel - Staff'), staff=staff)

#Need to test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_top_products(begin, end, limit):
    limitby = 10
    if limit != None:
        limitby = limit

    top_products = db.executesql("(SELECT product_id, count(*) as num_sales" \
                                 "FROM order_item" \
                                 "LEFT JOIN purchase_order ON order_item.purchase_order_no = purchase_order.purchase_order_no" \
                                 "WHERE purchase_order.sale_date >'"+ begin +"' AND purchase_order.sale_date <'" + end + "' GROUP BY product_id) ORDER BY num_sales limit by '" + limitby + "'")
    jp = json.dumps(top_products)
    return dict(chart=XML('<script>' + jp + '</script>'))

def get_sales_by_location(begin, end):

    sales_location = db.executesql("(SELECT guest.state, count(order_item.order_item_id) as sales"\
                                    "FROM order_item"\
                                    "LEFT JOIN purchase_order ON order_item.purchase_order_no = purchase_order.purchase_order_no"\
                                    "LEFT JOIN guest ON purchase_order.guest_id = guest.guest_id"\
                                    "WHERE purchase_order.sale_date > '11/11/2014' AND purchase_order.sale_date < '11/11/2015' GROUP BY guest.state)")