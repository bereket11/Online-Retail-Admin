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