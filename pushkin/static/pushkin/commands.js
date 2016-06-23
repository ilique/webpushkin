/**
 * Created by ilya on 19/04/16.
 */

$(document).ready(function(){

    $("#id_command_group").change(function(){
        var group_id = $(this).val();
        $("#commands-container").html("<img src='"+STATIC_URL+"/img/loader.gif'>");
        $.get(AJAX_URL + "?get=commands&command_group_id=" + group_id, function (data) {
            $("#commands-container").html(data);
        });
    });

    $("form").submit(function(e){
        e.preventDefault();
        var $output = $("#output-container");
        var result = [];
        var device_ip = $("#device_ip").val();
        var auth_param = $("#id_auth_param").val();
        var command_group = $("#id_command_group").val();
        var $commands = $(".commands");
        $output.html("<img src='"+STATIC_URL+"/img/loader.gif'>");

        $.each($commands, function(i, v){
            var line = '';
            var $parts = $(v).find("span");
            $.each($parts, function(i, v){
                if ($(v).find("input").length) {
                    line += $(v).find("input").val();
                } else {
                    line += $(v).html();
                }
            });

            result.push(line);
        });

        $.post(AJAX_URL, {
            commands: JSON.stringify(result),
            device_ip: device_ip,
            auth_param: auth_param,
            command_group: command_group,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}, function(data){

            $output.html(data);
        });

    });
});
