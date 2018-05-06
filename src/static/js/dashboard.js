let data = {
    "selection" : [],
    "selectable" : []
}
let config = {
    "large" : true,
    "select" : {
        "selectable" : false,
        "onlyFuture" : false,
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
url: "/api/v1/event/mine",
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
url: "/api/v1/user/dates/mine",
data: {},
dataType: "json",
cache: false,
beforeSend: function () {
    return true;
}
}).done(function (response) {
    updateSelectionInData("calendar-anker", response);
    reloadCalendar("calendar-anker");
    $("#write-selection-in-database").removeClass("loading");
}).fail(function (data) {
});

function writeSelectionInDatabase(){
    $.ajax({
        type: 'GET',
        url: "/api/v1/user/dates/update",
        data: returnCalendarSelected(anker),
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
