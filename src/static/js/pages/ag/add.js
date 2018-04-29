var agAddForm = $("#agAddForm");
$(agAddForm).submit(function (event) {
    // Stop the browser from submitting the form.
    event.preventDefault();
    var formData = $(agAddForm).serialize();
    $.ajax({
        type: 'POST',
        url: $(agAddForm).attr('action'),
        data: formData,
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#addag").addClass("loading");
            $("#name").removeClass("is-error");
            $("#name-error").hide();
            return true;
        }
    }).done(function (response) {
        window.location.href = response.redirect;
    }).fail(function (data) {
        $("#addag").removeClass("loading");
        switch (data.responseJSON.reason) {
            case "name":
                setNameError();
                break;
            case "display_name":
                break;
            case "description":
                break;
            default:
                $("#name").addClass("is-error");
        }
    });
    
});

var typingTimer;
var doneTypingInterval = 1000;
var $name = $('#name');

$name.on('input', function () {
    resetName();
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});




function doneTyping() {
    if (!$name.val()) return;
    $.ajax({
        type: 'GET',
        url: '/api/v1/ag/name/' + $name.val(),
        data: "{}",
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#name-loading").show();
        }
    }).done(function (response) {
        if (response && response.hasOwnProperty('name')) {
            setNameError()
        } else {
            setNameSuccess()
        }
    })
}

function resetName() {
    $name.removeClass("is-error");
    $name.removeClass("is-success");
    $("#name-check").hide();
}

function setNameError() {
    $("#name-loading").hide();
    $("#name-check").hide();
    $name.removeClass("is-success");
    $name.addClass("is-error");
}

function setNameSuccess() {
    $("#name-loading").hide();
    $("#name-check").show();
    $name.removeClass("is-error");
    $name.addClass("is-success");
}