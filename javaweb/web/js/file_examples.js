function example_submit(var1,var2){

    $('#hide_loading').show();

	var pic = var1;
	var data_type = var2;
	
	$.post("example_upload",
	   {
	       picture_name : pic,
		   type : data_type
	   },
	   function(return_data){
	
			if(data_type=='number'){json_number(return_data);}
			if(data_type=='plant'){json_plant(return_data);}
			if(data_type=='insect'){json_insect(return_data);}
			if(data_type=='yolo3'){json_yolo3(return_data);}
	
	
       }
    )}