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
            strData.append("type", "feature");
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
                type: "POST",  // post方法
                url: "/feature_analysis", // 调用feature_analysis路由
                processData: false,
                contentType: false,
                async: false,
                success: function (result) { // 获取服务器返回的res字典数组
                    var res = JSON.parse(result);//解析json
                    if(res['flag']=="false") //如果flag=false,给出错误提示
                    { alert(res['msg']); }
                    else
                    {
                        //遍历循环data数据，将结果展示到页面中
                        var strHtml = ""
                        for(var i = 0;i < res['data'].length;i++){//循环遍历数据
                            strHtml+='<a href="#" class="list-group-item list-group-item-success" id="res1">';
                            strHtml+='<span class="badge alert-success pull-right"></span>';
                            strHtml += res['data'][i]['type']+"： "+res['data'][i]['desc'];
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