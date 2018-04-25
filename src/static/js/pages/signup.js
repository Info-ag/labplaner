var signUpForm = $("#signUpForm");
    $(signUpForm).submit(function (event) {
        // Stop the browser from submitting the form.
        event.preventDefault();
        if ($("#password").val() == $("#password_rpt").val()) {
            var formData = $(signUpForm).serialize();
            $.ajax({
                type: 'POST',
                url: $(signUpForm).attr('action'),
                data: formData,
                dataType: "json",
                cache: false,
                beforeSend: function () {
                    $("#signUpFormFieldset").prop('disabled', true);
                    $("#signup").addClass("loading");
                    return true;
                },
                statusCode: function () {

                }
            }).done(function (response) {
                $("#signup").removeClass("loading");
                $.ajax({
                    type: 'POST',
                    url: '/auth/login',
                    data: formData,
                    dataType: "json",
                    cache: false
                }).done(function (response) {
                    window.location.href = response.redirect;
                })
            }).fail(function (data) {
                $("#signup").removeClass("loading");
                $("#signUpFormFieldset").prop('disabled', false);
            });
        } else {
            alert("Passwort stimmt nicht �berein");
            //Visualisieren statt dem Alert
        }

    });
