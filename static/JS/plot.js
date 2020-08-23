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
                        labelString: 'I, A'
                    },
                   
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Время'
                    }
                }]
            }
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
				  var jsonfile; // variable for json 
				  jsonfile = data;
                    var label = jsonfile.jsonarray.map(function(e) {
                       return e.xs;
                    });
                    var datas = jsonfile.jsonarray.map(function(e) {
                       return e.ys;
                    });;
                    chart.data.labels = label; //updating of chart labels
                    chart.data.datasets[0].data = datas; //updating of chart data
                    chart.update();
				});
				return false;
			  });
			});