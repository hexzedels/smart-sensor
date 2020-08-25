  var table = new Tabulator("#example-table", {
    height:"100%",
    layout:"fitColumns",
    columns:[
    {title:"Id", field:"id", widthGrow:0.5},
    {title:"Сила тока", field:"I",widthGrow:1},
    {title:"Напряжение", field:"U",widthGrow:1},
    {title:"Потребление", field:"P",widthGrow:1},
    {title:"Температура", field:"T", widthGrow:0.5},
    {title:"Max сила тока", field:"I_max", widthGrow:1},
    {title:"Max напряжение", field:"U_max", widthGrow:1},
    {title:"Время", field:"timecode", widthGrow:2},
    ],
});
$(function() { 
			  $('a#process_input').bind('click', function() { 
			  
				$.getJSON('/background_data', {
				  region: $('select[name="region"]').val(),
				  city: $('select[name="city"]').val(),
				  street: $('select[name="street"]').val(),
				  building: $('select[name="building"]').val(),
				  flat: $('select[name="flat"]').val(),
				  date_start: $('input[name="flatpick"]').val(),
				  date_end: $('input[name="flatpick1"]').val(),
				}, function(data) {
				    var jsonfile; // variable for json 
    				jsonfile = data;
                    var data = jsonfile.jsonarray;
                    table.replaceData(data);
				});
				return false;
			  });
			});