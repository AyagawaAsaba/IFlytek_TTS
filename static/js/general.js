document.querySelector("#file").onchange = function () {
        let reader = new FileReader();
        let file = this.files[0];
        //读取完成
        reader.onload = function (e) {
            //获取图片dom
            let img = document.querySelector("#img");
            //图片路径设置为读取的图片
            img.src = e.target.result;
            //上传文件
            var strData = new FormData();
            strData.append("upfile", file);
            strData.append("type", "general");
            $.ajax({
                type: "POST",
                url: "/upload",
                data: strData,
                processData: false,
                contentType: false,
                async: false,
                success: function (data) {
//                    alert('上传成功');
                },
               error: function (err) {
//               alert(err);
               }
            })
        };
        reader.readAsDataURL(file);
    };

$(".identifybutton").click(function(){
       $.ajax({
                type: "POST",
                url: "/general_api",
                processData: false,
                contentType: false,
                async: false,
                success: function (result) {
                    var res = JSON.parse(result);//解析json
                    if(res['flag']=="false")
                    {
                        alert(res['msg']);
                    }
                    else
                    {
                        var strHtml = ""
                        for(var i = 0;i < res['data'].length;i++){//循环遍历数据
                            strHtml+='<a href="#" class="list-group-item list-group-item-success" id="res1">';
                            strHtml+='<span class="badge alert-success pull-right"></span>';
                            strHtml += res['data'][i];
                            strHtml+='</a>';
                        }
                        $("#divAdd").html(strHtml);
                    }
                },
               error: function (err) {
                   alert(err);
               }
            })
});