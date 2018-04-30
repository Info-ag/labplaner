var today = new Date();

//buildBasis(today.getMonth() + 1, today.getFullYear(), "calendar-anker", {"size": true, "mode": 1});
configureCalendar('calendar-anker', {});
generateCalendar('calendar-anker');
$("#form-create-event").submit(function (event) {
    event.preventDefault();
    var formData = {
        ag: $("#ag").val(),
        display_name: $("#display_name").val(),
        description: $("#description").val(),
        dates: returnCalendarSelected("calendar-anker")
    }
    console.log(formData);
    $.ajax({
        type: 'POST',
        url: "/api/v1/event/",
        data: formData,
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#add-event").addClass("is-loading");
            return true;
        }
    }).done(function (response) {
        window.location.href = response.redirect;
    }).fail(function (data) {
        $("#add-event").removeClass("is-loading");
    });

});


