const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

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

function daysInMonth (month, year) {
    return new Date(year, month, 0).getDate();
}


var dateSelection = new Array();
var calendarMode;

//month from 0-11
function buildBasis(monthRaw, year, anker, options){
    month = monthRaw - 1;
    var div1 = $("<div></div>").addClass("calendar");
    if(options.hasOwnProperty('size')){
        var size = options.size;
        if(size == true){
            div1.addClass("calendar-lg");
        }
    }
    var divNav = $("<div></div>").addClass("calendar-nav navbar");
    var btnLeft = $("<button></button>").addClass("btn btn-action btn-link btn-lg").attr("id", anker+"-left");
    var iBtnLeft = $("<i></i>").addClass("icon icon-arrow-left");
    btnLeft.append(iBtnLeft);
    var divMonth = $("<div></div>").addClass("navbar-primary").attr("id", anker+"-heading").text(monthNames[month] + " " +  year);
    var btnRight = $("<button></button>").addClass("btn btn-action btn-link btn-lg").attr("id", anker+"-right");
    var iBtnRight = $("<i></i>").addClass("icon icon-arrow-right");
    btnRight.append(iBtnRight);

    var prevAndNextMonth = getPrevAndNextMonth(year, month);
    btnLeft.click({"year": prevAndNextMonth.previous.year, "month": prevAndNextMonth.previous.month, "anker": anker }, showAnotherMonth)
    btnRight.click({"year": prevAndNextMonth.next.year, "month": prevAndNextMonth.next.month, "anker": anker }, showAnotherMonth)
    divNav.append(btnLeft, divMonth, btnRight);
    var divContainer = $("<div></div>").addClass("calendar-container");
    var divHeader = $("<div></div>").addClass("calendar-header");
    var divMon = $("<div></div>").addClass("calendar-date").text("Mon");
    var divTue = $("<div></div>").addClass("calendar-date").text("Tue");
    var divWed = $("<div></div>").addClass("calendar-date").text("Wed");
    var divThu = $("<div></div>").addClass("calendar-date").text("Thu");
    var divFri = $("<div></div>").addClass("calendar-date").text("Fri");
    var divSat = $("<div></div>").addClass("calendar-date").text("Sat");
    var divSun = $("<div></div>").addClass("calendar-date").text("Sun");
    divHeader.append(divMon, divTue, divWed, divThu, divFri, divSat, divSun);
    var divBody = $("<div></div>").addClass("calendar-body").attr("id", anker + "-body");
    divBody = generateDays(year, month, anker, divBody, options);

    

    divContainer.append(divHeader, divBody);
    div1.append(divNav, divContainer);

    $("#" + anker).append(div1);
    if(options.hasOwnProperty("mode")){
        mode = options.mode;
        calendarMode = options.mode;
    }else{
        mode = 1;
        calendarMode = 1;
    }
    makeDaysSelectable();
    markToday();
    
}

function makeDaysSelectable(){
    if(calendarMode == 1){
        $(".calendar-date > .date-item").on("click", function(e){
            addSelection(this);
        })
    }
}


function showAnotherMonth(event){
    anker = event.data.anker;
    month = event.data.month;
    year = event.data.year;
    var divBody = $("#" + anker + "-body");
    divBody.empty();
    var prevAndNextMonth = getPrevAndNextMonth(year, month); 
    $("#" + anker + "-heading").text(monthNames[month] + " " +  year);
    $("#" + anker + "-right").off("click");
    $("#" + anker + "-left").off("click");
    $("#" + anker + "-left").click({"year": prevAndNextMonth.previous.year, "month": prevAndNextMonth.previous.month, "anker": anker }, showAnotherMonth)
    $("#" + anker + "-right").click({"year": prevAndNextMonth.next.year, "month": prevAndNextMonth.next.month, "anker": anker }, showAnotherMonth)
    divBody = generateDays(year, month, anker, divBody);
    makeDaysSelectable();
    markToday();
    if(calendarMode == 1){
        for (let i in dateSelection){
            $button = $("#"+dateSelection[i].replace(/\s/g,'-'));
            if($button.length != 0){
                $button.children("button").addClass("active");
                $button.children("button").off("click");
                $button.children("button").on("click", function(e){
                    removeSelection(this);
                })  
            }  
        }
    }
}


function markToday(){
    let today = new Date();
    let todayString = today.toDateString();
    console.log(todayString);
    if($("#"+todayString.replace(/\s/g,'-')).length != 0){
        console.log("test");
        $("#"+todayString.replace(/\s/g,'-')).children("button").addClass("date-today");
    }
}


function getPrevAndNextMonth(year, month){
    switch(month){
        case 0:
        return {"previous": {"year" : (year - 1), "month" : 11 }, "next": {"year" : (year), "month" : 1}};
        break;
        case 11:
        return {"previous": {"year" : year, "month" : 10}, "next": {"year" : (year + 1), "month" : 0}};
        break;
        default:
        return {"previous" : {"year" : year, "month" : (month - 1)}, "next": {"year" : year, "month" : (month + 1)}};

    }
}


function generateDays(year, month, anker, divBody, options){
    firstWeekDay = new Date(year, month).getDay();
    switch(firstWeekDay){
        case 0:
        var daysInPrevMonth = 6;
        break;
        case 1:
        var daysInPrevMonth = 7;
        break;
        default:
        var daysInPrevMonth = firstWeekDay - 1;
        
    }
    for( var i = ( - daysInPrevMonth) + 1 ; i <= 0; i++){
        var divDay = buildPrevDay(new Date(year, month, i));
        divBody.append(divDay);
    }

    lastDay = new Date(year, (month+1), 0);
    var lastDayNumber = lastDay.getDate();
    for (var i = 1; i <= lastDayNumber; i++){
        var divDay = buildCurrentDay(new Date(year, month, i));
        divBody.append(divDay);
    }
    lastWeekDay = lastDay.getDay();
    var daysInNextMonth = 7 - lastWeekDay;
    for (var i = 1; i <= daysInNextMonth; i++){
        var divDay = buildNextDay(new Date(year, (month + 1), i));
        divBody.append(divDay);
    }
    return divBody;
}

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

function addSelection(button){
    $button = $(button);
    dateSelection.push($button.attr("data-attr"));
    $button.addClass("active");
    $button.off("click");
    $button.on("click", function(e){
        removeSelection(this);
    })       
}

function removeSelection(button){
    $button = $(button);
    removeA(dateSelection, $button.attr("data-attr"));
    $button.removeClass("active");
    $button.off("click");
    $button.on("click", function(e){
        addSelection(this);
    })

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