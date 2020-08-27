			var canvas = document.getElementById('canvas')
                    var ctx = canvas.getContext('2d');
                    var config = {
                       type: 'line',
                       data: {
                          //labels: labels,
                          datasets: [{
                             label: 'Реальное потребление',
                             //data: [5, 1],
                             backgroundColor: 'rgba(0, 0, 0, 0)',
                             lineTension: 0,
                             borderColor: 'rgba(65, 131, 215, 0.8)'
                          },{
                             label: 'Спрогнозированное потребление',
                             //data: [ , , , , ,],
                             backgroundColor: 'rgba(0, 0, 0, 0)',
                             lineTension: 0,
                             borderColor: 'rgba(255,102,0,0.9)'//rgba(255, 131, 215, 0.8)
                          }],
                          //labels: ['0','1','2','3','4','5','6','7','8','9','11','11']
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
                        labelString: 'Потребление, кВт*час',
                    },
                   
                    ticks: {
                        beginAtZero:true,
                        //stepSize: 0.1,
                    }
                }],
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Время, ч'
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
			  
				$.getJSON('/background_analysis', {
				  date_start: $('input[name="flatpick"]').val(),
				}, function(data) {
				    console.log(data)
                    chart.data.labels = data.y; //updating of chart labels
                    chart.data.datasets[0].data = data.x1;
                    chart.data.datasets[1].data = data.x2; //updating of chart data
                    chart.update();
				});
				return false;
			  });
			});