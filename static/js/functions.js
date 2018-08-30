function load_materialize(){
    $('.timepicker').timepicker({'twelveHour':false, 'defaultTime': '00:00'});
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        i18n: {
            months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
            monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"],
            weekdays: ["Domingo","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            weekdaysShort: ["Dom","Lun", "Mar", "Mie", "Jue", "Vie", "Sab"],
            weekdaysAbbrev: ["D","L", "M", "M", "J", "V", "S"]
        }
    });
    $('.parallax').parallax();
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

function send_chain(first_element_id, first_url, chain_element_id, chain_url, redirect){
    var data_classroom = get_data($("#"+first_element_id)[0]);
    var classroom_id = send_form(first_url, data_classroom, false)["responseJSON"]["id"];
    var vector = $("#"+chain_element_id).find("form");
    for(a=0; a <= vector.length; a++){
        var data = get_data(vector[a]);
        data["id"] = classroom_id;
        send_form(chain_url, data, true);
    }
    window.location.replace(redirect)
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

function confirm_request(id, url, approved, element_id){
    if(confirm("Esta seguro?")){
        var other_id = $("#"+element_id).val()
        $.ajax({
            method:"POST",
            url:url,
            data:{
                'id':id,
                'approved': approved,
                'other_id': other_id,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            },
            success:function(){
                window.location.replace(url)
            },
            error: function(request, status, error){
                alert(request.responseText);
            }
        })
    }
}

function my_ajax(id, url, name, redirect){
    $.ajax({
        method:"POST",
        url:url,
        data:{
            'id':id,
            'name': name,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success:function(){
            window.location.replace(redirect)
        },
        error: function(request, status, error){
            alert(request.responseText);
        }
    });
}

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