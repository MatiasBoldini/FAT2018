function load_materialize(){
    $('select').formSelect();
    $('.timepicker').timepicker({'twelveHour':false, 'defaultTime': '00:00'});
};

function get_data(mElement){
    var data = { csrfmiddlewaretoken: getCookie('csrftoken') };
    var vector = mElement.find("input");
    for(a = 0; a < vector.length; a++){
        data[vector[a].name] = vector[a].value;  
    };
    console.log(data);
    return data;
}

function send_form(url, data){
    $.ajax({
        method : "POST",
        url: url,
        data:data,
        success: function(results){
            return(results);
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

function send_solo(url, element_id){
    var mElement = $("#"+element_id);
    send_form(url, get_data(mElement));
    // redirect to url
};

function send_chain(url, element_id, container_id, chain_url){
    var mElement = $("#"+element_id);
    var id = send_form(url, get_data(mElement));
    var vector = $("#"+container_id).find("form");
    for(a=0; a < vector.length; a++){
        var data = get_data($(vector[a]));
        data['id'] = id;
        send_form(vector[a], chain_url, data);
    }
    //redirect to url 
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
