var signUpForm = $("#logInForm");
$(signUpForm).submit(function (event) {
    event.preventDefault();
    var formData = $(signUpForm).serialize();
    $.ajax({
        type: 'POST',
        url: $(signUpForm).attr('action'),
        data: formData,
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#login").addClass("loading");
            $("#email").removeClass("is-error");
            $("#password").removeClass("is-error");
            $("#email-error").hide();
            return true;
        }
    }).done(function (response) {
        window.location.href = response.redirect;
    }).fail(function (data) {
        switch (data.responseJSON.reason) {
            case "email":
                $("#email").addClass("is-error");
                $("#email-error").show();
                break;
            case "password":
                $("#password").addClass("is-error");
                break;
            default:
                $("#password").addClass("is-error");
                $("#email").addClass("is-error");
        }
        $("#login").removeClass("loading");
    });

});


