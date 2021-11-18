
function postData(){
    //alert("hello");
    $('#hide_loading').show();


    var formData = new FormData();
    formData.append("photo",$("#photo")[0].files[0]);
    formData.append("service",'App.Passion.UploadFile');
    $.ajax({
        url:'upload', /*接口域名地址*/
        type:'post',
        data: formData,
        enctype: 'multipart/form-data',
        contentType: false,
        processData: false,
        success:function(return_data){
           json_number(return_data);

        }
    })
}



$(document).ready(function() {
    $('#hide_loading').hide();
    $('#hide_image').hide();
    $('#number_table').hide();




    // $("#file_submit").click(function() {
    //
    //
    //     var file = $("#file_input").val();
    //     $.post("upload",
    //         {
    //
    //             'myfile':file
    //         },
    //         function(data,status){
    //             alert("数据: \n" + data + "\n状态: " + status);
    //         });
    //
    // });

        //
        // $("#file_submit").click(function () {
        //
        //         var oInput = document.getElementById('file_input');
        //         var file = oInput.files[0];  //选取文件
        //         var formData = new FormData(); //创建表单数据对象
        //         formData.append('file',file); //将文件添加到表单对象中
        //     $.ajax({
        //         type: 'post',
        //         url: "upload", //上传文件的请求路径必须是绝对路劲
        //         data: formData,
        //         enctype: 'multipart/form-data'
        //     }).success(function (data) {
        //        // alert(data);
        //         alert("上传成功")
        //     }).error(function () {
        //         alert("上传失败");
        //     });
        // });


    // function submitForm() {
    //     console.log("submit event");
    //     var fd = new FormData(document.getElementById("fileinfo"));
    //    // fd.append("label", "WEBUPLOAD");
    //     $.ajax({
    //         url: "upload",
    //         type: "POST",
    //         data: fd,
    //         enctype: 'multipart/form-data',
    //         processData: false,  // tell jQuery not to process the data
    //         contentType: false   // tell jQuery not to set contentType
    //     }).done(function( data ) {
    //         console.log("Output:");
    //         console.log( data );
    //     });
    // }





});