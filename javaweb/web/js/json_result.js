function json_number(return_data){
	
		
	// alert("success");
	 //alert(data);
	
	 //return_data ='{"number": 2, "raw_data": [[2, 0.999], [8, 0.926], [3, 0.881], [1, 0.832], [7, 0.387], [6, 0.246], [4, 0.205], [0, 0.048], [9, 0.043], [5, 0.033]], "path": "img.png"}';
	 $('#hide_loading').hide();
	var  data = return_data;
	
	 var path = "./upload/"+data.path;
	 var number = data.number;
	 var value = data.raw_data;
	 //alert(path);
	
	
	 $("#input_image").attr("src",path);
	 $("#predict_result").html("预测的结果是： "+number);
	 $('#hide_image').show();
	
	 for(var i=0;i<10;i++) {
	     var x = document.getElementById("number_table").rows[i+1].cells;
	     x[0].innerHTML=value[i][0];
	     x[1].innerHTML=value[i][1];
	 }
	
	 $('#number_table').show();
		
	
}

function json_plant(return_data){
	
	
	// alert("success");
	            //alert(data);
	
	            //测试数据
				//return_data = '{"status": 0, "message": "OK", "results": [{"chinese_name": "唇形科_鼠尾草属_一串红", "latin_name": "Salvia splendens", "probability": 0.7113652229309082}, {"chinese_name": "大戟科_大戟属_一品红", "latin_name": "Euphorbia pulcherrima", "probability": 0.04702560976147652}, {"chinese_name": "菊科_向日葵属_千瓣葵", "latin_name": "Helianthus decapetalus", "probability": 0.005600047297775745}, {"chinese_name": "锦葵科_木槿属_朱槿", "latin_name": "Hibiscus rosa-sinensis", "probability": 0.005383869167417288}, {"chinese_name": "大戟科_麻风树属_琴叶珊瑚", "latin_name": "Jatropha integerrima", "probability": 0.005311214365065098}], "family_results": [{"chinese_name": "唇形科", "latin_name": "Lamiaceae", "probability": 0.7193701267242432}, {"chinese_name": "大戟科", "latin_name": "Euphorbiaceae", "probability": 0.05580082908272743}, {"chinese_name": "锦葵科", "latin_name": "Malvaceae", "probability": 0.025200219824910164}, {"chinese_name": "菊科", "latin_name": "Asteraceae", "probability": 0.021987145766615868}, {"chinese_name": "豆科", "latin_name": "Fabaceae", "probability": 0.01667122356593609}], "genus_results": [{"chinese_name": "唇形科_鼠尾草属", "latin_name": "Salvia", "probability": 0.7116087079048157}, {"chinese_name": "大戟科_大戟属", "latin_name": "Euphorbia", "probability": 0.04856305196881294}, {"chinese_name": "锦葵科_木槿属", "latin_name": "Hibiscus", "probability": 0.01594388857483864}, {"chinese_name": "菊科_向日葵属", "latin_name": "Helianthus", "probability": 0.008182854391634464}, {"chinese_name": "豆科_羊蹄甲属", "latin_name": "Bauhinia", "probability": 0.005516142584383488}], "image_name": "aaa.jpg"}';
	            $('#hide_loading').hide();
	            var  data = return_data;
	
	            var path = "./upload/"+data.image_name;
	           
			   var result = data.results;
			   var genus_results = data.genus_results;
			   var family_results = data.family_results;
	
				//alert(result);
				//将上传图片显示
	            $("#input_image").attr("src",path);
	            $("#predict_result").html("预测的结果是： "+result[0].chinese_name);
	            $('#hide_image').show();
				
	//********************************************//
	            for(var i=0;i<5;i++) {
	                var a = document.getElementById("plant_table_result").rows[i+1].cells; //i+1,除去表头
					var b = document.getElementById("plant_table_genus").rows[i+1].cells;
					var c = document.getElementById("plant_table_family").rows[i+1].cells;
					
	                a[0].innerHTML=result[i].chinese_name;
	                a[1].innerHTML=result[i].latin_name;
					a[2].innerHTML=Math.floor(result[i].probability*10000)/10000;
					
					b[0].innerHTML=genus_results[i].chinese_name;
					b[1].innerHTML=genus_results[i].latin_name;
					b[2].innerHTML=Math.floor(genus_results[i].probability*10000)/10000;
					
					c[0].innerHTML=family_results[i].chinese_name;
					c[1].innerHTML=family_results[i].latin_name;
					c[2].innerHTML=Math.floor(family_results[i].probability*10000)/10000;
	            }
	
	            $('#table_result').show();
	
	
	
}

function json_insect(return_data){
	
	// alert("success");
	            //alert(data);
	
	            //测试数据
				//return_data = '{"status": 0, "message": "OK", "results": [{"chinese_name": "鳞翅目_草螟科_褐萍水螟", "latin_name": "Cyrtogramme turbata", "probability": 0.8537358045578003}, {"chinese_name": "鳞翅目_螟蛾科_甜菜白带野螟", "latin_name": "Spoladea recurvalis", "probability": 0.007199340034276247}, {"chinese_name": "蜻蜓目_春蜓科_大团扇春蜓", "latin_name": "Sinictinogomphus clavatus", "probability": 0.002235256601125002}, {"chinese_name": "鳞翅目_凤蝶科_凤蝶属_宽带美凤蝶(宽带凤蝶)", "latin_name": "Papilio nephelus", "probability": 0.002033619675785303}, {"chinese_name": "鳞翅目_螟蛾科", "latin_name": "Pyralidae", "probability": 0.0017335580196231604}], "image_name": "mark_1.jpg"}';
	            $('#hide_loading').hide();
	            var  data = return_data;
	
	            var path = "./upload/"+data.image_name;
	
	            var result = data.results;
	            
	            //alert(result);
	            //将上传图片显示
	            $("#input_image").attr("src",path);
	            $("#predict_result").html("预测的结果是： "+result[0].chinese_name);
	            $('#hide_image').show();
	
	//********************************************//
	            for(var i=0;i<5;i++) {
	                var a = document.getElementById("plant_table_result").rows[i+1].cells; //i+1,除去表头
	                a[0].innerHTML=result[i].chinese_name;
	                a[1].innerHTML=result[i].latin_name;
	                a[2].innerHTML=Math.floor(result[i].probability*10000)/10000;
	
	            }
	
	            $('#table_result').show();
	
	
	
}

function json_yolo3(return_data){
	
	$('#hide_loading').hide();
	var  data = return_data;
		
	var path1 = "./upload/"+data.input;
		
	var path2 = "./upload/"+data.output;
	
	//alert(result);
	//将上传图片显示
	$("#input_image").attr("src",path1);
	$("#output_image").attr("src",path2);
	$('#hide_image').show();
	
	
	
}