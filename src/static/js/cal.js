//Calendar API



/*
HowToUse the API
Give any div you want to use as container an unique id. This id will be handled as "anker" in the following.
generate a JSON object describing all properties for the calendar. The config JSON object will be describded in the following.

config = {
    "anker" : <anker/id of the containing div (no default value - please just set any anker)>,
    "month" : <month to be shown (default : current month)>,
    "year" : <year of the month to be shown (default : current year)>,
    "size" : <0 for small | 1 for large> (default : 1),
    "mode" : <0 for selecting dates (with already selected dates) | 1 for showing events | 2 for both modes (default : 0),   //1 & 2 are not supported yet
    "selection" : < array'with the dates, that should be shown as already selected e.g. ["Sun Apr 01 2018", "Sun Apr 08 2018", "Sun Apr 15 2018", "Sun Apr 22 2018", "Sun Apr 29 2018"]>
}

call the configuring function with anker&config 
    configureCalendar(anker <anker>, config <config JSON Object>);

call the generating function with the anker
    generateCalendar(anker <anker>);

now you wait till you want the selected data and call the returning function
    return returnCalendarSelected(anker <anker>);


*/


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

//function to confire a calendar
function configureCalendar(anker, config){
    if(typeof anker == "undefined"){
        //Why do you calll this function without any anker?
        missingAnker();
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
    if(!config.hasOwnProperty("mode")){
        config.mode = 0;
    }
    if(config.mode == 0 || config.mode == 2){
        if(!config.hasOwnProperty("selection")){
            config.selection = new Array();
        }else{
            console.log(typeof config.selection);
        }
    }
    calendar[anker] = ({"name" : anker, "config": config});
}

//function to generate the calendar
function generateCalendar(anker){
    //first build the structure
    buildCalendarStructure(anker);
    //then insert the days
    buildCalendarDays(anker);
    //mark the current day
    markTodayInCalendar(anker);
    //make the days selectable - this will only be successful, if mode == 0 or 2
    makeCalendarDaysSelectable(anker);
}


function buildCalendarStructure(anker){
    //if there is no anker return
    if(!calendar.hasOwnProperty(anker)){
        return;
        missingAnker();
    }

    //load config
    let config = calendar[anker].config;


    //generate outer div
    let div1 = $("<div></div>").addClass("calendar");
    
    //check size and adapt
    if(config.size == 1){
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
        divBody.append(buildPrevDay(new Date(config.year, (config.month - 1), i)));
    }

    let lastDay = new Date(config.year, (config.month), 0);
    let lastDayNumber = lastDay.getDate();
    for (let i = 1; i <= lastDayNumber; i++){
        divBody.append(buildCurrentDay(new Date(config.year, (config.month - 1), i)));
    }
    let lastWeekDay = lastDay.getDay();
    let daysInNextMonth = 7 - lastWeekDay;
    for (let i = 1; i <= daysInNextMonth; i++){
        divBody.append(buildNextDay(new Date(config.year, (config.month), i)));
    }   
}


function buildPrevDay(day){
    div = $("<div></div>").addClass("calendar-date prev-month disabled");
    div = buildDay(day, div);
    return div;
};


function buildCurrentDay(day){
    div = $("<div></div>").addClass("calendar-date current-month");
    div = buildDay(day, div);
    return div;
}


function buildNextDay(day){
    div = $("<div></div>").addClass("calendar-date next-month disabled");
    div = buildDay(day, div);
    return div;
}


function buildDay(day, div){
    button = $("<button></button>").addClass("date-item").prop("type", "button").text(day.getDate());
    var dayString = day.toDateString(); 
    button.attr("data-attr", dayString);
    div.attr("id", dayString.replace(/\s/g,'-'));
    div.append(button);
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
    if(config.mode == 0){
        $("#" + anker + " .calendar-date > .date-item").on("click", {"anker" : anker}, function(e){
            addDayToSelection(this, e.data.anker);
        });
    }
}


function addDayToSelection(button, anker){
    let $button = $(button);
    calendar[anker].config.selection.push($button.attr("data-attr"));
    $button.addClass("active");
    $button.off("click");
    $button.on("click",{"anker" : anker}, function(e){
        removeDayFromSelection(this, e.data.anker);
    })     
}


function removeDayFromSelection(button, anker){
    let $button = $(button);
    removeA(calendar[anker].config.selection, $button.attr("data-attr"));
    $button.removeClass("active");
    $button.off("click");
    $button.on("click", {"anker" : anker}, function(e){
        addDayToSelection(this, e.data.anker);
    })

}


function returnCalendarSelected(anker){
    return calendar[anker].config.selection;
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
}


function loadAlreadySelectedDates(anker){
    let config = calendar[anker].config;
    for (let i in config.selection){
        $div = $("#"+anker + " #"+config.selection[i].replace(/\s/g,'-'));
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





//The following code is no implemented yet, it just stays here for some future features



function addEvents(events){

}

function addEvent(dayRaw, event, type){
    var dayString = dayRaw.toDateString();
    var divEventContainer = $("#" + dayString.replace(/\s/g,'-'));
    if(divEventContainer.children("calendar-events").length == 0){
        var divEvents = $("<div></div>").addClass("calendar-events");
        divEventContainer.append(divEvents);
    }else{ 
        var divEvents = divEventContainer.children(".calendar-events").first();    
    }
    if(event.hasOwnProperty("color")){
        var color = event.color;
    }else{
        var color = "error";
    }
    if(event.hasOwnProperty("display_name")){
        displayName = event.display_name;
    }else{
        displayName = "Something went wrong";
    }
    var aEvent = $("<a></a>").addClass("calendar-event text-light bg-"+color).text(displayName).attr("href", "#");
    divEventContainer.children(".calendar-events").first().append(aEvent);

    
}
