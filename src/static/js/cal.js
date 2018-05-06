//Calendar API



/*
HowToUse the API
Give any div you want to use as container an unique id. This id will be handled as "anker" in the following.
generate a JSON object describing all properties for the calendar. The config JSON object will be describded in the following.

config = {
    //"anker" : <anker/id of the containing div (no default value - please just set any anker)>,
    "month" : <month to be shown (default : current month)>,
    "year" : <year of the month to be shown (default : current year)>,
    "large" : <false/true (default true)>,
    "select" : {
        "selectable" : <false/true (default false)>,
        "onlyFuture" : <false/true (default true)>,
        "onlyCertainDates" : <false/true (default false)>
    },  
    "events" : {
        showDate: <false/true (default true)>, //
        showDates: <false/true (default false)>
    }
}

As third parameter you can use a data JSON object as following:

data = {
    "selection" : <array'with the dates, that should be shown as already selected e.g. ["Sun Apr 01 2018", "Sun Apr 08 2018", "Sun Apr 15 2018", "Sun Apr 22 2018", "Sun Apr 29 2018"]>,
    "selectable" : <array with the dates, that should be selectable (see config.select.onlycertainDates), same syntax as in selection>,
    "events" : [
        {
            "display_name" : <name of the event that should be displayed>,
            "id" : <id of the event>,
            "ag" : {
                "id" :
                "name" : 
            }
            "date" : <the day the event will take place>, // date the event will take place
            "color" : <css class (default primary)>,
            "dates" :  [ 
                {
                    "day" : "<day the event might is going to take place>",
                    "count" : <count how many users could come>;
                },
                {
                    "day" : "<another day the event might is going to take place>",
                    "count" : <count how many users could come>;
                },
            ]
        }
    ]
}

call the configuring function with anker&config 
    configureCalendar(anker <anker>, config <config JSON Object>, data <data JSON Object>);

call the generating function with the anker
    generateCalendar(anker <anker>);

now you wait till you want the selected data and call the returning function
    return returnCalendarSelected(anker <anker>);

    if you provide your dates in any other syntax than descripted, please use yourArray = validateDateArray(yourArray);

*/


function validateDateArray(dateArray){
    for(let i = 0; i < dateArray.length ; i++){
        dateArray[i] = new Date(new Date(dateArray[i]).setHours(0,0,0,0)).valueOf();
    }
    return dateArray;
}

function validateEventsData(anker){

}


//Variable to get monthname through month-number
const monthNames = ["","January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];


//helping function to delete an array element identified by the value
function removeA(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax= arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}


//Variable where all calenders, their config and data will be saved in
var calendar = {};

//functions for error messages
function missingAnker(){
    alert("Why do you call this function without any anker?");
}

function showError(msg){
    console.log(msg);
}

//function to confire a calendar
function configureCalendar(anker, config, data){
    if(typeof anker == "undefined"){
        //Why do you call this function without any anker?
        missingAnker();
    }
    if(typeof config == "undefined"){
        config = {};
    }
    if(typeof data == "undefined"){
        data = {};
    }
    if(!config.hasOwnProperty("month")){
        config.month = new Date().getMonth() + 1;
    }
    if(!config.hasOwnProperty("year")){
        config.year = new Date().getFullYear();
    }
    if(!config.hasOwnProperty("size")){
        config.size = 1;
    }
    if(!config.hasOwnProperty("select")){
        config.select = {};
    }
    if(!config.select.hasOwnProperty("selectable")){
        config.select.selectable = false;
    }
    if(!config.select.hasOwnProperty("onlyFuture")){
        config.select.onlyFuture = true;
    }
	if(!config.select.hasOwnProperty("onlyCertainDates")){
		config.select.onlyCertainDates = false;
	}
    if(!data.hasOwnProperty("selection")){
        data.selection = new Array();
    }else{
        console.log(typeof config.selection);
    }
	if(!data.hasOwnProperty("selectable")){
		data.selectable = new Array();
	}
    if(!data.hasOwnProperty("events")){
        data.events = new Array();
    }
    validateEventsData;
    calendar[anker] = ({"name" : anker, "config": config, "data": data});
}


//function to generate the calendar
function generateCalendar(anker){
    //first build the structure
    buildCalendarStructure(anker);
    //then insert the days
    buildCalendarDays(anker);
    //mark the current day
    markTodayInCalendar(anker);
    //make the days selectable - this will only be successful if config.select.selectable is set = true
    makeCalendarDaysSelectable(anker);
    showEvents(anker);
}


function buildCalendarStructure(anker){
    //if there is no anker return
    if(!calendar.hasOwnProperty(anker)){
        //return;
        missingAnker();
    }

    //load config
    let config = calendar[anker].config;


    //generate outer div
    let div1 = $("<div></div>").addClass("calendar");
    
    //check size and adapt
    if(config.large == true){
        div1.addClass("calendar-lg");
    }

    //generate calendar nav
    let divNav = $("<div></div>").addClass("calendar-nav navbar");


    //generate content of calendar nav
    let btnLeft = $("<button></button>").addClass("btn btn-action btn-link btn-lg").attr("id", anker+"-left").prop("type", "button");
    let iBtnLeft = $("<i></i>").addClass("icon icon-arrow-left");
    btnLeft.append(iBtnLeft);
    let divMonth = $("<div></div>").addClass("navbar-primary").attr("id", anker+"-heading").text(monthNames[config.month] + " " +  config.year);
    let btnRight = $("<button></button>").addClass("btn btn-action btn-link btn-lg").attr("id", anker+"-right").prop("type", "button");
    let iBtnRight = $("<i></i>").addClass("icon icon-arrow-right");
    btnRight.append(iBtnRight);

    //get prev and next month, so they can be accessed by the navbar buttons
    btnLeft.click({"anker": anker }, showPreviousCalendarMonth)
    btnRight.click({"anker": anker }, showNextCalendarMonth)
    divNav.append(btnLeft, divMonth, btnRight);

    //generate calendar inner container
    let divContainer = $("<div></div>").addClass("calendar-container");

    //generate calendar header with weekday headings
    let divHeader = $("<div></div>").addClass("calendar-header");
    let divMon = $("<div></div>").addClass("calendar-date").text("Mon");
    let divTue = $("<div></div>").addClass("calendar-date").text("Tue");
    let divWed = $("<div></div>").addClass("calendar-date").text("Wed");
    let divThu = $("<div></div>").addClass("calendar-date").text("Thu");
    let divFri = $("<div></div>").addClass("calendar-date").text("Fri");
    let divSat = $("<div></div>").addClass("calendar-date").text("Sat");
    let divSun = $("<div></div>").addClass("calendar-date").text("Sun");
    divHeader.append(divMon, divTue, divWed, divThu, divFri, divSat, divSun);
    //generate div body
    divBody = $("<div></div>").addClass("calendar-body").attr("id", anker + "-body");

    //finish setting up calendar structure
    divContainer.append(divHeader, divBody);
    div1.append(divNav, divContainer);
    $("#"+anker).append(div1);

}


function buildCalendarDays(anker){
    let config = calendar[anker].config;

    let divBody = $("#" + anker + "-body");
    divBody.empty();
    let daysInPrevMonth;
    let firstWeekDay = new Date(config.year, (config.month - 1)).getDay();
    switch(firstWeekDay){
        case 0:
        daysInPrevMonth = 6;
        break;
        case 1:
        daysInPrevMonth = 7;
        break;
        default:
        daysInPrevMonth = firstWeekDay - 1;
        
    }
    for( let i = ( - daysInPrevMonth) + 1 ; i <= 0; i++){
        divBody.append(buildPrevDay(new Date(new Date(config.year, (config.month - 1), i).setHours(0,0,0,0)), anker));
    }

    let lastDay = new Date(config.year, (config.month), 0);
    let lastDayNumber = lastDay.getDate();
    for (let i = 1; i <= lastDayNumber; i++){
        divBody.append(buildCurrentDay(new Date(new Date(config.year, (config.month - 1), i).setHours(0,0,0,0)), anker));
    }
    let lastWeekDay = lastDay.getDay();
    let daysInNextMonth = 7 - lastWeekDay;
    for (let i = 1; i <= daysInNextMonth; i++){
        divBody.append(buildNextDay(new Date(new Date(config.year, (config.month), i).setHours(0,0,0,0)), anker));
    }   
}


function buildPrevDay(day, anker){
    div = $("<div></div>").addClass("calendar-date prev-month disabled");
    div = buildDay(day, div, anker);
    return div;
};


function buildCurrentDay(day, anker){
    div = $("<div></div>").addClass("calendar-date current-month");
    div = buildDay(day, div, anker);
    return div;
}


function buildNextDay(day, anker){
    div = $("<div></div>").addClass("calendar-date next-month disabled");
    div = buildDay(day, div, anker);
    return div;
}


function buildDay(day, div, anker){
    let data = calendar[anker].data;
    let config = calendar[anker].config;
    button = $("<button></button>").addClass("date-item").prop("type", "button").text(day.getDate());
    var dayString = day.toDateString(); 
    button.attr("data-attr", dayString);
    div.attr("id", dayString.replace(/\s/g,'-'));
    if(config.select.onlyCertainDates == true){
        if(data.selectable.includes(day.valueOf())){
            button.attr("onlyselectable", true);
        }else{
            button.attr("onlyselectable", false)
			div.addClass("disabled");
        }
    }
    div.append(button);
    let divEventContainer = $("<div></div>").addClass("calendar-events");
    div.append(divEventContainer);    
    return div;
}


function markTodayInCalendar(anker){
    let todayString = new Date().toDateString();
    if($("#" + anker + " " +"#"+todayString.replace(/\s/g,'-')).length != 0){
        $("#"+todayString.replace(/\s/g,'-') + " > button").addClass("date-today");
    }
}


function makeCalendarDaysSelectable(anker){
    let config = calendar[anker].config;
    if(config.select.selectable == true){
        if(config.select.onlyFuture == true){
            if(config.select.onlyCertainDates == true){
                $("#" + anker + " .calendar-date > .date-item").filter(function(index){
                    return new Date($(this).attr("data-attr").replace("-", "")) >= new Date().setHours(0,0,0,0);
                }).filter(function(index){
                    return $(this).attr("onlyselectable");
                }).on("click", {"anker" : anker}, function(e){
                    addDayToSelection(this, e.data.anker);
                });
            }else{
                $("#" + anker + " .calendar-date > .date-item").filter(function(index){
                    return new Date($(this).attr("data-attr").replace("-", "")) >= new Date().setHours(0,0,0,0);
                }).on("click", {"anker" : anker}, function(e){
                    addDayToSelection(this, e.data.anker);
                });
            }
        }else if(config.select.onlyCertainDates == true){
            $("#" + anker + " .calendar-date > .date-item").filter(function(index){
                return ("true" == $(this).attr("onlyselectable"));
			}).on("click", {"anker" : anker}, function(e){
                addDayToSelection(this, e.data.anker);
            });
        }else{
            $("#" + anker + " .calendar-date > .date-item").on("click", {"anker" : anker}, function(e){
                addDayToSelection(this, e.data.anker);
            });

        }
    }
}


function addDayToSelection(button, anker){
    let $button = $(button);
    calendar[anker].data.selection.push($button.attr("data-attr"));
    $button.addClass("active");
    $button.off("click");
    $button.on("click",{"anker" : anker}, function(e){
        removeDayFromSelection(this, e.data.anker);
    })     
}


function removeDayFromSelection(button, anker){
    let $button = $(button);
    removeA(calendar[anker].data.selection, $button.attr("data-attr"));
    $button.removeClass("active");
    $button.off("click");
    $button.on("click", {"anker" : anker}, function(e){
        addDayToSelection(this, e.data.anker);
    })

}


function returnCalendarSelected(anker){
    return calendar[anker].data.selection;
}


function showPreviousCalendarMonth(event){
    let anker = event.data.anker;
    let config = calendar[anker].config;
    if(config.month == 1){
        config.month = 12;
        config.year--;
    }else{
        config.month--;
    }
    showNewCalendarMonth(anker);
}


function showNextCalendarMonth(event){
    let anker = event.data.anker;
    let config = calendar[anker].config;
    if(config.month == 12){
        config.month = 1;
        config.year++;
    }else{
        config.month++;
    }
    showNewCalendarMonth(anker);
}


function showNewCalendarMonth(anker){
    buildCalendarDays(anker);
    $("#" + anker + "-heading").text(monthNames[calendar[anker].config.month] + " " + calendar[anker].config.year);
    markTodayInCalendar(anker);
    makeCalendarDaysSelectable(anker); 
    loadAlreadySelectedDates(anker);
    showEvents(anker);
}


function loadAlreadySelectedDates(anker){
    let data = calendar[anker].data;
    for (let i in data.selection){
        $div = $("#"+anker + " #"+data.selection[i].replace(/\s/g,'-'));
        $button = $div.children("button");
        if($button.length != 0){
            $button.addClass("active");
            $button.off("click");
            $button.on("click",{"anker" : anker}, function(e){
                removeDayFromSelection(this, e.data.anker);
            })     
        }  
    }
}

function updateSelectionInData(anker, selection){
    calendar[anker].data.selection = selection;
}

function updateEventsInData(anker, events){
    calendar[anker].data.events = events;     
}

function reloadCalendar(anker){
    buildCalendarDays(anker);
    $("#" + anker + "-heading").text(monthNames[calendar[anker].config.month] + " " + calendar[anker].config.year);
    markTodayInCalendar(anker);
    makeCalendarDaysSelectable(anker); 
    loadAlreadySelectedDates(anker);
    showEvents(anker);
}

function showEvents(anker){
    let data = calendar[anker].data;
    let config = calendar[anker].config;
    for(let i = 0; i < data.events.length; i++){
        if(config.events.showDate == true){
            if(data.events[i].date){
                showDate(anker, i);
            }
        }
        if(config.events.showDate == true){
            if(data.events[i].dates.length != 0){
                showDates(anker, i);
            }
        }
    }
}

function showDate(anker, i){
    let data = calendar[anker].data;
    addEvent(anker, i, new Date(data.events[i].date).toDateString(), false);
}

function showDates(anker, i){
    let data = calendar[anker].data;
    let config = calendar[anker].config;
    for(let k = 0; k < data.events[i].dates.length; k++){
        addEvents(anker, i, data.events[i].dates[k], true);
    }    
}




function addEvent(anker, i, dateString){
    let data = calendar[anker].data;
    var divEventContainer = $("#" + dateString.replace(/\s/g,'-')).children(".calendar-events").first();
    if(divEventContainer.length == 0){
        return;
    }
    if(!data.events[i].hasOwnProperty("display_name")){
        data.events[i].display_name = "Something went wrong";
    }
    if(!data.events[i].ag.hasOwnProperty("color")){
        data.events[i].ag.color = "primary";
    }
    let aEvent = $("<a></a>").addClass("has-icon-right text-light calendar-event bg-"+data.events[i].ag.color).text(" " + data.events[i].display_name).attr("href", "/ag/"+ data.events[i].ag.name +"/event/"+data.events[i].id);
    let icon = $("<i></i>").addClass("icon icon-check");
    aEvent.prepend(icon);
    divEventContainer.append(aEvent);
}

function addEvents(anker, i, date){
    let data = calendar[anker].data;
    dateString = new Date(date.day).toDateString();
    var divEventContainer = $("#" + dateString.replace(/\s/g,'-')).children(".calendar-events").first();
    if(divEventContainer.length == 0){
        return;
    }
    if(!data.events[i].hasOwnProperty("display_name")){
        data.events[i].display_name = "Something went wrong";
    }
    if(!data.events[i].ag.hasOwnProperty("color")){
        data.events[i].ag.color = "primary";
    }
    let aEvent = $("<a></a>").addClass("has-icon-right text-light calendar-event bg-"+data.events[i].ag.color).text(date.count+": " + data.events[i].display_name).attr("href", "/ag/"+ data.events[i].ag.name +"/event/"+data.events[i].id);
    divEventContainer.append(aEvent);     
}
