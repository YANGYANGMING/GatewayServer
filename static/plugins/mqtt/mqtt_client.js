
// 将在全局初始化一个 mqtt 变量
    //console.log(mqtt);
    
    // 连接选项
    const options = {
        connectTimeout: 4000, // 超时时间
        // 认证信息
        username: 'ORISONIC',
        password: 'ORISONIC2020',
    };

    // const client = mqtt.connect('ws://121.36.220.210:8083/mqtt', options);
    const client = mqtt.connect('ws://192.168.0.41:8083/mqtt', options);
    // const client = mqtt.connect('ws://www.yymit.cn:8083/mqtt', options);
    // const client = mqtt.connect('wss://www.yymit.cn:8084/mqtt', options);
    // const client = mqtt.connect('wss://192.168.0.41:8084/mqtt', options);

    // client.
    client.on('connect', (error) => {
        console.log('链接成功:', error)
    });
    client.on('reconnect', (error) => {
        console.log('正在重连:', error)
    });
    
    client.on('error', (error) => {
        console.log('连接失败:', error)
    });

    // 订阅列表
    client.subscribe('pub', { qos: 2 });
    // 监听接收消息事件
    client.on('message', (topic, message) => {
        // console.log('收到来自', topic, '的消息', message.toString());
        var payload = eval("(" + message.toString() + ")");
        var id = payload.id;
        var header = payload.header;
        var msg = payload.msg;

        if (id === 'client') {
            // console.log('收到来自', topic, '的消息');
            var status = payload.status;
            $('#' + header).html(msg);

            if (header === 'gwdata') {
                if (status) {
                    ClearMSGAndRefersh('#' + header);
                }else{
                    button_sample = false;
                }
            }else if (
                header === 'update_sensor' ||
                header === 'add_sensor' ||
                header === 'remove_sensor'
            ) {
                if (status){
                    ClearMSGAndJump('#' + header);
                }
            }else if (header === 'set_sensor_params') {

                if (status){
                    setTimeout(function () {
                    $('#' + header).text('');
                    window.location.href="/GWS/edit-sensor-params";
                }, 1500);
                }
            }
        }

    });
    
    // client.publish('0.0.2.0', '{"header": "gwdata"}', (error) => {
    //     console.log(error || '消息发布成功')
    // });
