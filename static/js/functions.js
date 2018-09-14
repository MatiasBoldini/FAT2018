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

function get_data(form, model_name){
    var form_data = new FormData(form);
    var results = {'model':model_name};
    for(var data of form_data.entries()){
        results[data[0]] = data[1];
    }
    return results;
}

function create_model(form_id, url, model_name){
    var form = $("#"+form_id).get(0)
    $.ajax({
        method: "POST",
        url:url,
        data:get_data(form, model_name),
        success: function(results){
            alert(results)
        },
        error: function(request){
            switch(request.status) {
                case 400:
                alert("Error interno contactar con administradores")
            }
        }
    });
}

function model_and_id(url, model_name, model_id){
    $.ajax({
        method: "POST",
        url:url,
        data:{
            'model':model_name,
            'model_id':model_id,
            'csrfmiddlewaretoken':getCookie('csrftoken')
        },
        success: function(results){
            alert(results)
        },
        error: function(request){
            switch(request.status) {
                case 405:
                alert("Error interno contactar con administradores")
            }
        }
    });
}

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