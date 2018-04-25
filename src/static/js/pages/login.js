var signUpForm = $("#logInForm");
    $(signUpForm).submit(function (event) {
        // Stop the browser from submitting the form.
        event.preventDefault();
        var formData = $(signUpForm).serialize();
        $.ajax({
            type: 'POST',
            url: $(signUpForm).attr('action'),
            data: formData,
            dataType: "json",
            cache: false,
            beforeSend: function () {
                $("#logInFormFieldset").prop('disabled', true);
                $("#login").addClass("loading");
                return true;
            },
            statusCode: function () {

            }
        }).done(function (response) {
            $("#login").removeClass("loading");
            console.log(response);
            window.location.href = response.redirect;
        }).fail(function (data) {
            console.log(data);
            $("#login").removeClass("loading");
            $("#signUpFormFieldset").prop('disabled', false);
        });

    });


