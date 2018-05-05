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
