/**

   Created and copyrighted by Massimo Di Pierro <massimo.dipierro@gmail.com>
   (MIT license)  

   Example:

   <script src="share.js"></script>

**/

jQuery(function(){
	var script_source = jQuery('script[src*="share.js"]').attr('src');
        var params = function(name,default_value) {
            var match = RegExp('[?&]' + name + '=([^&]*)').exec(script_source);
            return match && decodeURIComponent(match[1].replace(/\+/g, ' '))||default_value;
        }
	var path = params('static','social');
	var url = encodeURIComponent(window.location.href);
	var host =  window.location.hostname;
	var title = escape(jQuery('title').text());
	var twit = 'http://twitter.com/home?status='+title+'%20'+url;
	var facebook = 'http://www.facebook.com/sharer.php?u='+url;
	var gplus = 'https://plus.google.com/share?url='+url;
	var tbar = '<div id="socialdrawer"><span>Share<br/></span><div id="sicons"><a href="'+twit+'" id="twit" title="Share on twitter"><img src="'+path+'/twitter.png"  alt="Share on Twitter" width="32" height="32" /></a><a href="'+facebook+'" id="facebook" title="Share on Facebook"><img src="'+path+'/facebook.png"  alt="Share on facebook" width="32" height="32" /></a><a href="'+gplus+'" id="gplus" title="Share on Google Plus"><img src="'+path+'/gplus-32.png"  alt="Share on Google Plus" width="32" height="32" /></a></div></div>';	
	// Add the share tool bar.
	jQuery('body').append(tbar); 
	var st = jQuery('#socialdrawer');
	st.css({'opacity':'.7','z-index':'3000','background':'#FFF','border':'solid 1px #666','border-width':' 1px 0 0 1px','height':'20px','width':'40px','position':'fixed','bottom':'0','right':'0','padding':'2px 5px','overflow':'hidden','-webkit-border-top-left-radius':' 12px','-moz-border-radius-topleft':' 12px','border-top-left-radius':' 12px','-moz-box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)','-webkit-box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)','box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)'});
	jQuery('#socialdrawer a').css({'float':'left','width':'32px','margin':'3px 2px 2px 2px','padding':'0','cursor':'pointer'});
	jQuery('#socialdrawer span').css({'float':'left','margin':'2px 3px','text-shadow':' 1px 1px 1px #FFF','color':'#444','font-size':'12px','line-height':'1em'});
        jQuery('#socialdrawer img').hide();
	// hover
	st.click(function(){
		jQuery(this).animate({height:'40px', width:'160px', opacity: 0.95}, 300);
		jQuery('#socialdrawer img').show();
	    });
	//leave
	st.mouseleave(function(){ 
	    st.animate({height:'20px', width: '40px', opacity: .7}, 300); 
	    jQuery('#socialdrawer img').hide();
	    return false;
	    }  );
    });

function product_add($id) {
	 $.ajax({
		 type: "POST",
		 url: "/Admin_Panel/default/add_product?id="+$id,
	 }).done(function (e) {
		 respond =  JSON.parse(e);
		 if(respond.response == 1){
			 alert_add_cart('Product successfully added to inventory.');
		 }


	 })




}

function product_edit(event) {
	var element = "<textarea id=text_title_"+event+">"+$('#title_'+event).html()+"</textarea>";
	element+="<input type='button' value='SAVE' onclick='product_save("+event+")'>";
	$('#title_'+event).html(element)

	// var element = "<textarea id=text_price_"+event+">"+$('#price_'+event).html()+"</textarea>";
	// $('#price_'+event).html(element)

	// var element = "<textarea id=text_cost_"+event+">"+$('#cost_'+event).html()+"</textarea>";
	// $('#cost_'+event).html(element)

	var element = "<textarea id=text_desc_"+event+">"+$('#desc_'+event).html()+"</textarea>";
	$('#desc_'+event).html(element)

	// var element = "<textarea id=text_manufacturer_"+event+">"+$('#manufacturer_'+event).html()+"</textarea>";
	// $('#manufacturer_'+event).html(element)

	// var element = "<textarea id=text_supplier_sku_"+event+">"+$('#supplier_sku_'+event).html()+"</textarea>";
	// $('#supplier_sku_'+event).html(element)
    //
	// var element = "<textarea id=text_supplier_name_"+event+">"+$('#supplier_name_'+event).html()+"</textarea>";
	// $('#supplier_name_'+event).html(element)


	// var element = "<textarea id=text_size_"+event+">"+$('#size_'+event).html()+"</textarea>";
	// $('#size_'+event).html(element)

	// var element = "<textarea id=text_color_"+event+">"+$('#color_'+event).html()+"</textarea>";
	// $('#color_'+event).html(element)
}


function product_save($id) {
	// console.log($id)
	$title = escape(document.getElementById('text_title_'+$id).value);
	$desc = escape(document.getElementById('text_desc_'+$id).value);
	// $price = escape(document.getElementById('text_price_'+$id).value);
	// $supplier_sku = escape(document.getElementById('text_supplier_sku_'+$id).value);
	// $supplier_name = escape(document.getElementById('text_supplier_name_'+$id).value);
	// $manufacturer = escape(document.getElementById('text_manufacturer_'+$id).value);

	// $cost = escape(document.getElementById('text_cost_'+$id).value);
	$.ajax({
		 type: "POST",
		 url: "/Admin_Panel/default/edit_product?id="+$id+"&title="+$title+"&desc="+$desc,
	 })
	location.reload();
}

$('#supplier_list').on('change',function (e) {
	document.getElementById('supplier_table').innerHTML = '';
	// $('#dropDownId :selected').text();
	var id = $('#supplier_list :selected').val();
	var general1 = "<select";
	var general2 = "><option value='null'></option>" +
		"<option value='title'>title</option>" +
		"<option value='description'>description</option>" +
		"<option value='manufacturer'>manufacturer</option>" +
		"<option value='upc'>UPC</option>" +
		"<option value='length'>length</option>" +
		"<option value='height'>height</option>" +
		"<option value='unit'>unit</option>" +
		"<option value='width'>width</option>" +
		"<option value='created_by'>created_by</option>" +
		"<option value='create_date'>create_date</option>" +
		"<option value='weight'>weight</option></select>";


	$.ajax({
		 type: "POST",
		 url: "/Admin_Panel/default/load_supplier_data?id="+id,
	 })
		.done(function (respond) {

			var data = $.parseJSON(respond);
			var count = 0;
			var fields = [];
			data.forEach(function (e) {
				count++;
				fields.push(e['column_name']);
			})


			for($i=0;$i<count;$i++){
				$('#supplier_table').html($('#supplier_table').html() + '<tr><td>'+fields[$i]+'</td><td id='+fields[$i]+'>'+general1+' id='+fields[$i]+' '+general2+'</td></tr>')
			}
			$('#supplier_table').show();
			$('#normalize_btn').show();
		})


	
})

$('#normalize_btn').on('click',function (e) {
	var dest = '';
	var source = '';
	$supplier_id = $('#supplier_list').find(':selected').val();
	$('#supplier_table tr td:nth-child(2)').each(function () {
		var id = this.id;
		var equivalent = $('#' + id).find(':selected').val();
		source += id + ', '
		dest += equivalent + ', '
	});

	source = '(' + source.replace(/, $/, ")")
	dest = '(' + dest.replace(/. $/, ")")

	$.ajax({
		type: "POST",
		url: "/Admin_Panel/default/set_normalize?source=" + source + '&dest=' + dest+'&supplier_id='+$supplier_id
	})
		.done(function (respond) {
			alert_add_cart('Supplier data has been successfully normalized');
		})
})

var tags, all_tags;
var check;

function tag_opener($id) {
	tag_open($id)
}

function tag_open($id) {
	var status = $('#tag_choose_'+$id).css('display');
	if(status != 'none'){
		$('#tag_choose_'+$id).hide();
		$('#tag_choose_'+$id+'.tag_choose').css('height','0px');
		return
	}


	$.ajax({
		type: "POST",
		url: "/Admin_Panel/default/load_tags?pid=" + $id,
	})
		.done(function (respond) {
			tags = JSON.parse(respond);
			options = ''
			for(i=0 ; i< tags.length; i++){
				value = tags[i]['tag_name']
				check = tags[i]['tag_association_id']
				if(check != null){
					options+= "<input type='checkbox' checked='checked' value="+value+">"+value+"</input><br>"
				}else{
					options+= "<input type='checkbox' value="+value+">"+value+"</input><br>"
				}
			}
			$('#select_'+$id).html(options)
			if(status == 'none'){
				$('#tag_choose_'+$id).show();
				$('#tag_choose_'+$id+'.tag_choose').css('height','200px');
			}

	})
}

$('.inline').on('click', function (e) {
	if(this.id == 'tab1'){
		$('#tab2_container').hide();
		$('#tab1_container').show();
	}else{
		$('#tab1_container').hide();
		$('#tab2_container').show();
	}
})


function tag_save() {
	var tag = escape($('#add_tag_box').val());
	$.ajax({
		type: "POST",
		url: "/Admin_Panel/default/tag_save?tag="+tag,
	})
		.done(function (respond) {
			console.log(respond)
		})
}

function save_tag($id) {
	var set_values = ''
	console.log($id);
	$('#select_'+$id+' input').each(function() {
    	set_values += $(this).attr('value')+' = '+this.checked+' , ';
	});
	set_values = set_values.replace(/, $/, "")
	set_values = escape(set_values)
	$.ajax({
		type: "POST",
		url: "/Admin_Panel/default/new_tag_save?tags="+set_values+'&pid='+$id,
	})
	.done(function (respond) {
		console.log(respond)
	})
}

function image_opener(pid) {
	if( $('#img_place_'+pid).html() != ''){
		$('#img_place_'+pid).fadeOut(1000);
		$('#img_place_'+pid).html('');
		$('#img_place_'+pid).fadeIn();

		return false
	}
	$('#img_place_'+pid).html("<img width='250px' src='/Admin_Panel/static/images/loading.gif'> <span style='color: #569eea;font-size: 1.6em;font-weight: bold'>Loading Images Please Wait...</span>");
	setTimeout(function(){ extracted(pid); }, 2500);

}

function extracted(pid){
            $.ajax({
                type: "POST",
                url: "/Admin_Panel/default/load_image?pid="+pid,
            })
                .done(function (respond) {
                    respond =  JSON.parse(respond);
                    img_obj = '';
                    for(i=0; i<respond.length; i++){
                        img_path = respond[i]['image_path'];
                        img_default = respond[i]['default'];
                        img_id = respond[i]['image_id'];
                        if(img_default == '1'){
                            img_obj += "<input checked='checked' type='radio' name='img_select_"+pid+"' value='"+img_id+"'><img width='150' src=../static/images/product_images/"+img_path+".jpg>"
                        }else{
                            img_obj += "<input type='radio' name='img_select_"+pid+"' value='"+img_id+"'><img width='150' src=../static/images/product_images/"+img_path+".jpg>"
                        }

                    }
                    img_obj += "<input style='margin-left: 20px' type=button class='button_save' value='save' onclick='image_save_default("+pid+")'>"
                    $('#img_place_'+pid).html(img_obj)
                })
        }

function image_save_default(pid) {
	var selected = $("input[name='img_select_"+pid+"']:checked").val();
	$.ajax({
		type: "POST",
		url: "/Admin_Panel/default/save_default_image?pid="+pid+"&img_id="+selected,
	})
	.done(function (respond) {
		alert_add_cart('Main image has been successfully saved.')
	})
}


function alert_add_cart(msg){
	$('#cart_alert').css('visibility','visible')
	$('#msg_container #msg').html(msg)
    $("#cart_alert").fadeIn(50);
}

$('body').on('click',function () {
	$("#cart_alert").fadeOut(0);
})

function close_add_cart(){
    $("#cart_alert").fadeOut(0);
}

(function(){
    $("#cart_alert").fadeOut(0);
})();

$('.main_icon').on('click',function (e) {
	window.location = e.target.id
})