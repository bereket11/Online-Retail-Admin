# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def chart():
    dados_chart="[{name: 'Batata', y: 12},{name: 'Tomate', y: 8},{name: 'Mamão', y: 12}]" #Change this dynamically
    dados_map={}
    dados_map["dados"]=dados_chart
    chart="""
    <script type="text/javascript">
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
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Meu Gráfico'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        credits:{enabled:false},
        series: [{
            name: 'Vendar por porcentagem',
            colorByPoint: true,
                data: %(dados)s
                }]
            });
    </script>
    """ %dados_map
    return dict(chart=XML(chart))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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
