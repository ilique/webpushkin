$(document).ready(function () {

    $("#id_service").change(function () {

        var service_id = $(this).val();

        $("#service-description-container").html("<img src='" + STATIC_URL + "/img/loader.gif'>");

        $.get(AJAX_URL + "?get=services&service_id=" + service_id, function (data) {

            $("#service-description-container").html(data).on('change', '.command-groups', function(){

                var group_id = $(this).val();
                var $container = $(this).next();

                $container.html("<img src='"+STATIC_URL+"/img/loader.gif'>");

                $.get(AJAX_URL + "?get=commands&command_group_id=" + group_id, function (data) {
                    $container.html(data);
                });
                
            }).on('click', '.add-service-device', function(e){

                e.preventDefault();

                var $container = $(this).parents(".service-device-and-commands");

                // duplicate device and its command groups
                $container.parent().append("<div class='service-device-and-commands'>"+$container.html()+"</div>");
            });

        });

    });

    $("form").submit(function (e) {

        e.preventDefault();
        
        var service = [];
        var $output = $("#output-container");

        $output.html("<img src='"+STATIC_URL+"/img/loader.gif'>");

        $(".device_ips").each(function(i, device){
            
            var command_lines = [];
            var $device = $(device);
            var ip = $device.val();
            var auth_id = $device.parent().next().find(".auth-params").val();
            var model_id = $device.siblings(".model-names").val();

            $device.parent().next().next().children("li").each(function (i, commands) {
                $(commands).find(".commands").each(function(i, v){

                    var line = '';
                    var $parts = $(v).find("span");
                    
                    $.each($parts, function(i, v){
                        if ($(v).find("input").length) {
                            line += $(v).find("input").val();
                        } else {
                            line += $(v).html();
                        }
                    });

                    command_lines.push(line);

                })
            });

            service.push({
                'device_ip': ip,
                'auth_id': auth_id,
                'model_id': model_id,
                'commands': command_lines
            });
        });

        console.log(service);

        $.post(AJAX_URL, {service: JSON.stringify(service), csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}, function(data){
            
            console.log(data);
            $output.html(data);
            
        })
    });
});
