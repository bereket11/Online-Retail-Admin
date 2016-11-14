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
	 })
	console.log($id)

}

function product_edit(event) {
	var element = "<textarea id=text_title_"+event+">"+$('#title_'+event).html()+"</textarea>";
	element+="<input type='button' value='SAVE' onclick='product_save("+event+")'>";
	$('#title_'+event).html(element)

	var element = "<textarea id=text_price_"+event+">"+$('#price_'+event).html()+"</textarea>";
	$('#price_'+event).html(element)

	var element = "<textarea id=text_cost_"+event+">"+$('#cost_'+event).html()+"</textarea>";
	$('#cost_'+event).html(element)

	var element = "<textarea id=text_desc_"+event+">"+$('#desc_'+event).html()+"</textarea>";
	$('#desc_'+event).html(element)

	var element = "<textarea id=text_manufacturer_"+event+">"+$('#manufacturer_'+event).html()+"</textarea>";
	$('#manufacturer_'+event).html(element)

	var element = "<textarea id=text_supplier_sku_"+event+">"+$('#supplier_sku_'+event).html()+"</textarea>";
	$('#supplier_sku_'+event).html(element)

	var element = "<textarea id=text_supplier_name_"+event+">"+$('#supplier_name_'+event).html()+"</textarea>";
	$('#supplier_name_'+event).html(element)


	var element = "<textarea id=text_size_"+event+">"+$('#size_'+event).html()+"</textarea>";
	$('#size_'+event).html(element)

	var element = "<textarea id=text_color_"+event+">"+$('#color_'+event).html()+"</textarea>";
	$('#color_'+event).html(element)
}


function product_save($id) {
	console.log($id)
	$title = escape(document.getElementById('text_title_'+$id).value);
	$desc = escape(document.getElementById('text_desc_'+$id).value);
	$price = escape(document.getElementById('text_price_'+$id).value);
	$supplier_sku = escape(document.getElementById('text_supplier_sku_'+$id).value);
	$supplier_name = escape(document.getElementById('text_supplier_name_'+$id).value);
	$manufacturer = escape(document.getElementById('text_manufacturer_'+$id).value);
	$color = escape(document.getElementById('text_color_'+$id).value);
	$size = escape(document.getElementById('text_size_'+$id).value);
	$cost = escape(document.getElementById('text_cost_'+$id).value);
	$.ajax({
		 type: "POST",
		 url: "/Admin_Panel/default/edit_product?id="+$id+"&title="+$title+"&desc="+$desc+"&price="+$price+"&cost="+$cost+"&color="+$color+"&size="+$size+"&manufacturer="+$manufacturer+"&supplier_sku="+$supplier_sku+"&supplier_name="+$supplier_name,
	 })
	location.reload();
}