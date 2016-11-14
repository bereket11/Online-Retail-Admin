$(document).ready(function(){
   $("#submit_supplier").hide();
});

function show_supplier_form(){
    $("#submit_supplier").show();
}
function hide_supplier_form(){
    $("#submit_supplier").hide();
}

function show_supplier_edit_form(id){
    console.log("#edit_supplier_"+id);
    $("#edit_supplier_"+id).show();
}

function hide_supplier_edit_form(id){
    console.log("#edit_supplier_"+id);
    $("#edit_supplier_"+id).hide();
}