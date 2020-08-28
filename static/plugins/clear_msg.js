//清除提示信息
    function ShowErrorMSG(nid) {
        setTimeout(function () {
            $(nid).text('操作失败，网关未响应！')
        }, 6000);
    }

//清除提示信息并跳转
    function ClearMSGAndJump(nid) {
        setTimeout(function () {
            $(nid).text('');
            window.location.href="/GWS/sensor-manage";
        }, 1500);
    }

//清除提示信息并刷新
    function ClearMSGAndRefersh(nid) {
        setTimeout(function () {
            $(nid).text('');
            // window.location.reload();
        }, 3000);
    }


// 显示失败信息
    function SetTimeToShowTimeOutMSG(ele_id, gwntid) {
        setTimeout(function () {
            $("#" + ele_id).html('操作失败，网关未响应！');
            client.publish(gwntid, '{"header": ' + ele_id + ', "msg": "操作失败，网关未响应！", "id": "client", "status": 0}', function(error) {
                console.log(error || '消息发布成功，操作失败，网关未响应！')
            });
        }, 8000);

     }



