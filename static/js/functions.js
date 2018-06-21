function load_materialize(){
    $('.timepicker').timepicker({'twelveHour':false, 'defaultTime': '00:00'});
    $('select').formSelect();
};

function get_data(form){
    var form_data = new FormData(form);
    var results = {};
    for(var data of form_data.entries()){
        results[data[0]] = data[1];
    }
    return results;
}

function send_form(url, data, wait){
    return $.ajax({
        method : "POST",
        url: url,
        data:data,
        async: wait,
        success: function(results){
            console.log(results)
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
};

function send_solo(url, element_id){
    send_form(url, new FormData($("#"+element_id)), true);
    window.location.replace(url)
};

function remove(url, id){
    $.ajax({
        url: url,
        data:{
            'id': id
        },
        success: function(results){
            $("#"+id).remove()
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
};

function send_chain(first_element_id, first_url, chain_element_id, chain_url){
    var data_classroom = get_data($("#"+first_element_id)[0]);
    var classroom_id = send_form(first_url, data_classroom, false)["responseJSON"]["id"];
    var vector = $("#"+chain_element_id).find("form");
    for(a=0; a <= vector.length; a++){
        var data = get_data(vector[a]);
        data["id"] = classroom_id;
        send_form(chain_url, data, true);
    }
    window.location.replace(first_url)
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

function load_form_data(url, element_id, id){
    $.ajax({
        url: url,
        data : {
            'id':id
        },
        success: function(results){
            $("#"+element_id).html(results);
            load_materialize();
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
};

function load_chain_data(url, element_id, id){
    var new_div = document.createElement('div');
    new_div.className = 'row chain';
    $('#' + element_id).append(new_div); 
    $.ajax({
        url: url,
        data : {
            'id':id
        },
        async: false,
        success: function(results){
            $('.chain').last().html(results);
            load_materialize();
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
}