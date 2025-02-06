function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        const $this = $(this);
        const name = $("input[name='name']").val();
        const email = $("input[name='email']").val();

        if (!email) {
            alert("请先输入邮箱！");
            return;
        }

        // Disable the button during the AJAX request
        $this.prop("disabled", true);
        console.log("Email:", email);

        // 通过js发送网络请求：ajax。Async JavaScript And XML（JSON）
        // Jinja2
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:21658/user/captcha?name=" + encodeURIComponent(name) + "&email=" + encodeURIComponent(email),
            data: {
                "name": name,
                "email": email
            },

            success: function (res) {
                console.log('Success: ', res);
                const code = res['code'];
                if (code === 200) {
                    // 取消点击事件
                    //    $this.off("click");
                    // 开始倒计时
                    let countDown = 60;
                    // const timer = setInterval(function () {
                    //     countDown -= 1;
                    //     if (countDown > 0) {
                    //         $this.text(countDown + "秒后重新发送");
                    //     } else {
                    //         $this.text("获取验证码");
                    //         $this.prop("disabled", false);
                    //         // 重新执行下这个函数，重新绑定点击事件
                    //         bindCaptchaBtnClick();
                    //         // 如果不需要倒计时了，那么就要记得清除倒计时，否则会一直执行下去
                    //         clearInterval(timer);
                    //     }
                    // }, 1000);

                    const timer = function countdown() {
                        countDown -= 1;
                        if (countDown > 0) {
                            $this.text(countDown + "秒后重新发送");
                            setTimeout(countdown, 1000);

                        } else {
                            $this.text("获取验证码");
                            $this.prop("disabled", false);
                        }
                    };
                    timer();  // Start the countdown
                    // 提示
                    alert("验证码发送成功！");

                } else if (code === 400) {
                    alert(res['message']);
                } else {
                    // Handle other response codes if needed
                    alert("Unexpected response code: " + code);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error in the AJAX request:", status, error);
                alert("An unexpected error occurred. Please try again.\n" + "Error:" + error);
                $this.prop("disabled", false);
            }

        })
    });
}


// 等网页文档所有元素都加载完成后再执行
$(function () {
    bindCaptchaBtnClick();
});

