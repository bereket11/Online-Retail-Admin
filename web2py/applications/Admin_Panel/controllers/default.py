# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to the Admin Panel!")
    return dict(location=T('Admin Panel - Index'))

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

def page2():
    return dict(location=T('Admin Panel - Page 2'))

def page3():
    return dict(location=T('Admin Panel - Page 3'))

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
