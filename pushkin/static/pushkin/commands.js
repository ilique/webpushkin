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

    $("form").submit(function(){
        var result = [];

        var $commands = $(".commands");
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

        console.log(encodeURI(result.join("\n")));
        $("#commands").val(result.join("#delimeter#"));

    });
});
