$(document).ready(function(){
   $("#submit_supplier").hide();
});

function show_supplier_form(){
    $("#submit_supplier").show();
    $("#supplier_add_button").hide();
}
function hide_supplier_form(){
    $("#submit_supplier").hide();
    $("#supplier_add_button").show();
}

function show_supplier_edit_form(id){
    console.log("#edit_supplier_"+id);
    $("#edit_supplier_"+id).show();
}

function hide_supplier_edit_form(id){
    console.log("#edit_supplier_"+id);
    $("#edit_supplier_"+id).hide();
}

function show_staff_edit_form(id){
    console.log("#edit_staff_"+id);
    $("#edit_staff_"+id).show();
}

function hide_staff_edit_form(id){
    console.log("#edit_staff_"+id);
    $("#edit_staff_"+id).hide();
}

function set_stat_tab(num){
    switch(num){
        case '1': console.log("tab1");
            $("#report-tab1").css({'background':'#112294'});
            $("#report-tab2").css({'background':'#5aff94'});
            $("#report-tab3").css({'background':'#5aff94'});
            $("#report-tab4").css({'background':'#5aff94'});
            $("#report-chart1").css({'z-index':'5','display':'inline'});
            $("#report-chart2").css({'z-index':'1','display':'none'});
            $("#report-chart3").css({'z-index':'1','display':'none'});
            $("#report-chart4").css({'z-index':'1','display':'none'});
            break;
        case '2':  console.log("tab2");
            $("#report-tab1").css({'background':'#5aff94'});
            $("#report-tab2").css({'background':'#112294'});
            $("#report-tab3").css({'background':'#5aff94'});
            $("#report-tab4").css({'background':'#5aff94'});
            $("#report-chart1").css({'z-index':'1','display':'none'});
            $("#report-chart2").css({'z-index':'5','display':'inline','width':'100%'});
            $("#report-chart3").css({'z-index':'1','display':'none'});
            $("#report-chart4").css({'z-index':'1','display':'none'});
            break;
        case '3': console.log("tab3");
            $("#report-tab1").css({'background':'#5aff94'});
            $("#report-tab2").css({'background':'#5aff94'});
            $("#report-tab3").css({'background':'#112294'});
            $("#report-tab4").css({'background':'#5aff94'});
            $("#report-chart1").css({'z-index':'1','display':'none'});
            $("#report-chart2").css({'z-index':'1','display':'none'});
            $("#report-chart3").css({'z-index':'5','display':'inline','width':'100%'});
            $("#report-chart4").css({'z-index':'1','display':'none'});
            break;
        case '4': console.log("tab4");
            $("#report-tab1").css({'background':'#5aff94'});
            $("#report-tab2").css({'background':'#5aff94'});
            $("#report-tab3").css({'background':'#5aff94'});
            $("#report-tab4").css({'background':'#112294'});
            $("#report-chart1").css({'z-index':'1','display':'none'});
            $("#report-chart2").css({'z-index':'1','display':'none'});
            $("#report-chart3").css({'z-index':'1','display':'none'});
            $("#report-chart4").css({'z-index':'5','display':'inline','width':'100%'});
            break;
    }
}