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
            strData.append("type", "itr");
            $.ajax({
                type: "POST",
                url: "/upload",
                data: strData,
                processData: false,
                contentType: false,
                async: false,
            })
        };
        reader.readAsDataURL(file);
    };

$(".identifybutton").click(function(){
       $.ajax({
                type: "POST",
                url: "/itr_api",
                processData: false,
                contentType: false,
                async: false,
                success: function (result) {
                    var res = JSON.parse(result);//解析json
                    if(res['flag']==="false")
                    {
                        alert(res['msg']);
                    }
                    else
                    {
                        var total=res['right']+res['wrong'];
                        var strHtml = ""

                        strHtml+='<a href="#" class="list-group-item list-group-item-success" id="res1">';
                        strHtml+='<span class="badge alert-success pull-right"></span>';
                        strHtml += '总共 '+total+" 题";
                        strHtml+='</a>';
                        strHtml+='<a href="#" class="list-group-item list-group-item-success" id="res1">';
                        strHtml+='<span class="badge alert-success pull-right"></span>';
                        strHtml += '错误 '+res['wrong']+" 题";
                        strHtml+='</a>';

                        $("#divAdd").html(strHtml);
                        //获取图片dom
                        let img = document.querySelector("#img2");
                        //图片路径设置为读取的图片
                        var now = new Date().getTime();
                        // img.src = res['path']+'?'+now;
                        // img.src = res['path'];
                        img.src = './static/images/upload/itr_result.jpg';
                        console.log(res['msg']);
                        console.log(img.src);
                    }
                },
               error: function (err) {
                   alert(err);
               }
            })
});