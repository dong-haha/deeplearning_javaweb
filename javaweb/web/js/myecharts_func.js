function first_echarts(rawdata,w,b,max){
	
	var line='y = '+w+'* x + '+b;
	
	
	var markLineOpt = {
	  label: {
	    formatter: line,
	    align: 'top'
	  },
	  lineStyle: {
	    type: 'solid',
		color:"#000000",
	  },
	  tooltip: {
	    formatter: line
	  },
	  data: [
	    [
	      {
	        coord: [0, b],
	        symbol: 'none'
	      },
	      {
	        coord: [max, max*w+b],
	        symbol: 'none'
	      }
	    ]
	  ]
	};
	

		var chartDom_1 = document.getElementById('echarts_1');
		var myChart_1 = echarts.init(chartDom_1);
		var option_1;
		
		option = {
			title: {   
			  text: '原始数据和模拟的直线方程' ,
			  left: 'center',
			    top: 0
			
			},
			
			grid: { left: '10%', top: '10%',right:'10%',bottom: '10%' ,width: '70%', height: '70%' },
			
		  xAxis: { name: 'x值', },
		  yAxis: {name: 'y值',},
		  
		  series: [
		    {
		      symbolSize: 5,
		      data: obj1.raw_data,
		      type: 'scatter',
			  color:'red',
			  markLine: markLineOpt
		    }]
		};
		
		option && myChart_1.setOption(option);

	
}

function second_echarts(W_arr){
	//alert(W_arr);
	
	var chartDom = document.getElementById('echarts_2');
	var myChart_2 = echarts.init(chartDom);
	var option;
	
	option = {
		title: {
		  text: 'W值随训练次数变化' ,
		  left: 'center',
		    top: 0
		
		},
		grid: { left: '10%', top: '10%',right:'10%',bottom: '10%' ,width: '70%', height: '70%' },
	  xAxis: {
	    name:'训练次数',
	  },
	  yAxis: {
	    name:'W值',
	  },
	  series: [
	    {
	      data: W_arr,
	      type: 'line',
	    }
	  ]
	};
	
	option && myChart_2.setOption(option);
	
	
}

function third_echarts(b_arr){
	//alert(W_arr);
	
	var chartDom = document.getElementById('echarts_3');
	var myChart_3 = echarts.init(chartDom);
	var option;
	
	option = {
		title: {
		  text: 'b值随训练次数变化' ,
		  left: 'center',
		    top: 0
		
		},
		grid: { left: '10%', top: '10%',right:'10%',bottom: '10%' ,width: '70%', height: '70%' },
	  xAxis: {
	    name:'训练次数',
	  },
	  yAxis: {
	    name:'b值',
	  },
	  series: [
	    {
	      data: b_arr,
	      type: 'line',
	    }
	  ]
	};
	
	option && myChart_3.setOption(option);
	
	
}





function four_echarts(loss){
	//alert(W_arr);
	
	var chartDom = document.getElementById('echarts_4');
	var myChart_4 = echarts.init(chartDom);
	var option;
	
	option = {
		title: {
		  text: 'loss随训练次数变化' ,
		  left: 'center',
		    top: 0
		
		},
		grid: { left: '10%', top: '10%',right:'10%',bottom: '10%' ,width: '70%', height: '70%' },
	  xAxis: {
	    name:'训练次数',
	  },
	  yAxis: {
	    name:'loss',
	  },
	  series: [
	    {
	      data: loss,
	      type: 'line',
	    }
	  ]
	};
	
	option && myChart_4.setOption(option);
	
	
}