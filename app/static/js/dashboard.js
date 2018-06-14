let data = {
    "selection" : [],
    "selectable" : []
}
let config = {
    "large" : false,
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
url: selfEventsUrl,
data: {},
dataType: "json",
cache: false,
beforeSend: function () {
    return true;
}
}).done(function (response) {
    updateEventsInData("calendar-anker", response.events);
    reloadCalendar("calendar-anker");
}).fail(function (data) {
});

$.ajax({
type: 'GET',
url: selfGetDatesUrl,
data: {},
dataType: "json",
cache: false,
beforeSend: function () {
    return true;
}
}).done(function (response) {
    if(typeof calendar["calendar-anker"].data.selection == undefined){
        calendar["calendar-anker"].data.selection = new Array();
    }
    for (let i = 0; i < response.dates.length ; i++){
        calendar["calendar-anker"].data.selection[calendar["calendar-anker"].data.selection.length] =  (new Date(response.dates[i].day)).toDateString();
    }
    reloadCalendar("calendar-anker");
    $("#write-selection-in-database").removeClass("loading");
}).fail(function (data) {
});

$("#write-selection-in-database").on("click", function(){
    writeSelectionInDatabase("calendar-anker");
})

function writeSelectionInDatabase(anker){
    $.ajax({
        type: 'POST',
        url: selfSetDatesUrl,
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
