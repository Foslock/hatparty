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
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



function claimHat(hat_id) {
    if (hat_id) {
        $.post("/wearhat/" + hat_id).done(function(data) {
            console.log(data);
            _refreshData();
        });
    }
}

function ditchHat(hat_id) {
    if (hat_id) {
        $.post("/ditchhat/" + hat_id).done(function(data) {
            console.log(data);
            _refreshData();
        });
    }
}

function likeHat(hat_id) {
    if (hat_id) {
        $.post("/likehat/" + hat_id).done(function(data) {
            console.log(data);
            _refreshData();
        });
    }
}

function slapUser(user_id) {
    if (user_id) {
        $.post("/slapuser/" + user_id).done(function(data) {
            console.log(data);
            _refreshData();
        });
    }
}

function _refreshData() {
    $.get("/hatdata").done(function(data) {
        var slaps = data['slaps'];
        console.log(data);
    });
}


$(document).ready(
function(){

    CURRENT_USER = "me";

    console.log("It's hat time.");

    _refreshData();
});