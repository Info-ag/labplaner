let data = {
    "selection" : [],
    "selectable" : []
}
let config = {
    "large" : true,
    "select" : {
        "selectable" : true,
        "onlyFuture" : true,
        "onlyCertainDates" : false
    },
    "events" : {
        showDate: true,
        showDates: true
    }
}
configureCalendar('calendar-anker', config, data);
generateCalendar('calendar-anker');

$.ajax({
type: 'GET',
url: "/api/v1/user/self/events",
data: {},
dataType: "json",
cache: false,
beforeSend: function () {
    return true;
}
}).done(function (response) {
    updateEventsInData("calendar-anker", response);
    reloadCalendar("calendar-anker");
}).fail(function (data) {
});

$.ajax({
type: 'GET',
url: "/api/v1/user/self/dates",
data: {},
dataType: "json",
cache: false,
beforeSend: function () {
    return true;
}
}).done(function (response) {
    updateSelectionInData("calendar-anker", response.dates);
    console.log(response);
    reloadCalendar("calendar-anker");
    $("#write-selection-in-database").removeClass("loading");
}).fail(function (data) {
});

function writeSelectionInDatabase(anker){
    $.ajax({
        type: 'POST',
        url: "/api/v1/user/self/dates",
        data: {"dates" : returnCalendarSelected(anker)},
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#write-selection-in-database").addClass("loading");
        }
        }).done(function (response) {
            $("#write-selection-in-database").removeClass("loading");
        }).fail(function (data) {

        });
}
