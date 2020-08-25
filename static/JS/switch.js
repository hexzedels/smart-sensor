$(function() { 
    $('#rg').change(function() { 
        $.getJSON('/background_select', {
            region: $('select[name="region"]').val(),
        },
        function(data) {
            var select = document.getElementById('city');
            var array = data.city;
            //Create and append the options
            for (i = select.options.length-1; i >= 0; i--) {
                select.options[i] = null;
            }
            for (var i = 0; i < array.length; i++) {
                
                var option = document.createElement("option");
                option.value = array[i];
                option.text = array[i];
                select.appendChild(option);
            }
            document.getElementById("city").style.display = "";
        });
    });
    $('#city').change(function(){
        document.getElementById("street").style.display = "";
    });
    $('#street').change(function(){
        document.getElementById("building").style.display = "";
    });
    $('#building').change(function(){
        document.getElementById("flat").style.display = "";
    });
});