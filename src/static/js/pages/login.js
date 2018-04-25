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
            statusCode: function (
            
            ) {

            }
        }).done(function (response) {
            $("#login").removeClass("loading");
            window.location.href = response.redirect;
        }).fail(function (data) {
            $(".form-group").removeClass("has-error");
            $(".form-input-hint").addClass("d-invisible");
            console.log(data.responseJSON.reason);
            switch(data.responseJSON.reason) {
                case "email":      
                    $("#emailP").removeClass("d-invisible");
                    $("#emailGroup").addClass("has-error");
                    break;
                case "password":
                    $("#passwordP").removeClass("d-invisible");
                    $("#passwordGroup").addClass("has-error");
                    break;
                default:
                    alert("something went wrong entirely");
            }
            $("#login").removeClass("loading");
            $("#logInFormFieldset").prop('disabled', false);
        });

    });


