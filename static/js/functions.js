function load_materialize(){
    $('select').formSelect();
    $('.timepicker').timepicker({'twelveHour':false, 'defaultTime': '00:00'});
};

function send_form(element_id, url){
    var data = { csrfmiddlewaretoken: getCookie('csrftoken') };
    var vector = $("#"+element_id).find("input");
    for(a = 0; a < vector.length; a++){
        data[vector[a].name] = vector[a].value;  
    };
    $.ajax({
        method : "POST",
        url: url,
        data:data,
        success: function(results){
            alert("works")
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
};

function load_part(url, place){
    $.ajax({
        url: url,
        success: function(results){
            place.html(results);
            load_materialize();
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
};
function load_chain(url, place){
    var new_div = document.createElement('div');
    new_div.className = 'row chain';
    $('#' + place).append(new_div); 
    load_part(url, $('.chain').last());
};

function load_solo(url, place){
    load_part(url, $("#"+place));
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
