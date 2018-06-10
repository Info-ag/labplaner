var today = new Date();
config = {
    "large" : true,
    "select" : {
        "selectable" : true,
        "onlyFuture" : true
    },  
    "events" : {
        showAll: false
    }
}
configureCalendar('calendar-anker', config);
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
        url: eventUrl,
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


