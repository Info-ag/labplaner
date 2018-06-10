var signUpForm = $("#signUpForm");
$(signUpForm).submit(function (event) {
    // Stop the browser from submitting the form.
    event.preventDefault();
    if ($("#password").val() === $("#password_rpt").val()) {
        var formData = $(signUpForm).serialize();
        $.ajax({
            type: 'POST',
            url: $(signUpForm).attr('action'),
            data: formData,
            dataType: "json",
            cache: false,
            beforeSend: function () {
                $("#signup").addClass("loading");
                $("#email").removeClass("is-error");
                $("#email-error").hide();
                $("#password").removeClass("is-error");
                $("#password-error").hide();
                return true;
            }
        }).done(function () {
            $.ajax({
                type: 'POST',
                url: loginUrl,
                data: formData,
                dataType: "json",
                cache: false
            }).done(function (response) {
                window.location.href = response.redirect;
            })
        }).fail(function (data) {
            $("#signup").removeClass("loading");
            switch (data.responseJSON.reason) {
                case "username":
                    setNameError();
                    break;
                case "email":
                    $("#email").addClass("is-error");
                    $("#email-error").show();
                    break;
                case "password":
                    $("#password").addClass("is-error");
                    $("#password-error").show();
                    break;
                default:
                    $("#name").addClass("is-error");
                    $("#password").addClass("is-error");
                    $("#email").addClass("is-error");
            }
        });
    }
});

var typingTimer;
var doneTypingInterval = 1000;
var $username = $('#name');
var $pwd = $('#password_rpt');

$username.on('input', function () {
    resetName();
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

$pwd.on('input', function () {
    if ($pwd.val() !== $("#password").val()) {
        $("#password_rpt").addClass("is-error");
        $("#password_rpt-error").show();
    } else {
        $("#password_rpt").removeClass("is-error");
        $("#password_rpt-error").hide();
    }
});


function doneTyping() {
    if (!$username.val()) return;
    $.ajax({
        type: 'GET',
        url: '/api/v1/user/username/' + $username.val(),
        data: "{}",
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#name-loading").show();
        }
    }).done(function (response) {
        if (response && response.hasOwnProperty('username')) {
            setNameError()
        } else {
            setNameSuccess()
        }
    })
}

function resetName() {
    $username.removeClass("is-error");
    $username.removeClass("is-success");
    $("#name-check").hide();
}

function setNameError() {
    $("#name-loading").hide();
    $("#name-check").hide();
    $username.removeClass("is-success");
    $username.addClass("is-error");
}

function setNameSuccess() {
    $("#name-loading").hide();
    $("#name-check").show();
    $username.removeClass("is-error");
    $username.addClass("is-success");
}