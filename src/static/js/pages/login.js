var signUpForm = $("#logInForm");
    var formMessages = $("#formMessages");
    $(signUpForm).submit(function (event) {
        // Stop the browser from submitting the form.
        event.preventDefault();
        if ($("#password").val() == $("#password_rpt").val()) {
            var formData = $(signUpForm).serialize();
            console.log(formData);
            $.ajax({
                type: 'POST',
                url: $(signUpForm).attr('action'),
                data: formData,
                dataType: "json",
                cache: false,
                beforeSend: function () {
                    $("#signUpFormFieldset").prop('disabled', true);
                    formMessages.text("Anfrage wurde gesendet, es wird auf eine Antwort gewartet.");
                    $("#signup").addClass("loading");
                    return true;
                },
                statusCode: function () {

                }
            }).done(function (response) {
                $("#signup").removeClass("loading");
                $.ajax({
                    type: 'POST',
                    url: '{{ url_for('auth.login') }}',
                    data: formData,
                    dataType: "json",
                    cache: false
                }).done(function (response) {
                    window.location.href = response.redirect;
                })
            }).fail(function (data) {
                $("#signup").removeClass("loading");
                $("#signUpFormFieldset").prop('disabled', false);
                formMessages.text("Irgendetwas lief falsch");
            });
        } else {
            alert("Passwort stimmt nicht überein");
            //Visualisieren statt dem Alert
        }

    });

