			var canvas = document.getElementById('canvas')
                    var ctx = canvas.getContext('2d');
                    var config = {
                       type: 'line',
                       data: {
                          //labels: labels,
                          datasets: [{
                             label: 'Сила тока',
                             //data: data,
                             backgroundColor: 'rgba(0, 0, 0, 0)',
                             lineTension: 0,
                             borderColor: 'rgba(65, 131, 215, 0.8)'
                          }]
                       },
                       options: {
                       tooltips: {
                mode: 'index',
                intersect: false
            },
            scales: {
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Ток, А',
                    },
                   
                    ticks: {
                        //beginAtZero:true
                    }
                }],
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Время'
                    }
                }]
            },
            annotation: { }
            }
                    };
                    
var chart = new Chart(ctx, config);
/*
Next function gets json from /background_plot node as a reply on sent params
*/
$(function() { 
			  $('a#process_input').bind('click', function() { 
			  
				$.getJSON('/background_plot', {
				  region: $('select[name="region"]').val(),
				  city: $('select[name="city"]').val(),
				  street: $('select[name="street"]').val(),
				  building: $('select[name="building"]').val(),
				  flat: $('select[name="flat"]').val(),
				  dep: $('select[name="dep"]').val(),
				  date_start: $('input[name="flatpick"]').val(),
				  date_end: $('input[name="flatpick1"]').val(),
				}, function(data) {
                    document.getElementById("dep").style.display = "";
                    document.getElementById("typee").style.display = ""; 
                    document.getElementById("depend").style.display = "";  
                    var jsonfile; // variable for json 
				    var success = {
                                    drawTime: "afterDraw",
                                    annotations: [{
                                    type: 'line',
                                    mode: 'horizontal',
                                    scaleID: 'y-axis-0',
                                    value: 220,
                                    borderColor: 'tomato',
                                    borderWidth: 1.5,
                                    }]
                                  };
                    jsonfile = data;
                    var label = jsonfile.jsonarray.map(function(e) {
                       return e.xs;
                    });
                    var datas = jsonfile.jsonarray.map(function(e) {
                       return e.ys;
                    });;
                    if ((jsonfile.labelarray.labelString == "U, В") || (jsonfile.labelarray.labelString == "U_max, В")) {
                        chart.options.annotation = success
                    } else {
                        chart.options.annotation = {}
                    };
                    
                    chart.data.datasets[0].label = jsonfile.labelarray.label;
                    chart.options.scales.yAxes[0].scaleLabel.labelString = jsonfile.labelarray.labelString;
                    chart.options.scales.xAxes[0].scaleLabel.labelString = jsonfile.labelarray.xlabelString;
                    chart.data.labels = label; //updating of chart labels
                    chart.data.datasets[0].data = datas; //updating of chart data
                    chart.update();
				});
				return false;
			  });
			});