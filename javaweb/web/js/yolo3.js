
function postData(){
    //alert("hello");
    $('#hide_loading').show();


    var formData = new FormData();
    formData.append("photo",$("#photo")[0].files[0]);
    formData.append("service",'App.Passion.UploadFile');
    $.ajax({
        url:'uploadyolo3', /*接口域名地址*/
        type:'post',
        data: formData,
        enctype: 'multipart/form-data',
        contentType: false,
        processData: false,
        success:function(return_data){
           json_yolo3(return_data);

        }
    })
}



$(document).ready(function() {
    $('#hide_loading').hide();
    $('#hide_image').hide();
    $('#number_table').hide();
    $('#table_result').hide();






});