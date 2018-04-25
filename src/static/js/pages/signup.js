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
                    $("#passwordP").text("");
                    $("#password_rptGroup").removeClass("has-error");
                    $("#signup").addClass("loading");
                    console.log("rest");
                    return true;
                }
            }).done(function (response) {
                console.log("rest");
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
            $("#passwordP").text("your input must match your first password input");
            $("#password_rptGroup").addClass("has-error");
            $("#password_rpt").change(function(){
                if($("#password").val() == $("#password_rpt").val()){      
                    $("#passwordP").text("");
                    $("#password_rptGroup").removeClass("has-error");
                    $("#password_rptGroup").addClass("has-success");
                }else{
                    $("#passwordP").text("your input must match your first password input");
                    $("#password_rptGroup").addClass("has-error");
                    $("#password_rptGroup").removeClass("has-success");
                    
                }
            })
            //Visualisieren statt dem Alert
        }

    });