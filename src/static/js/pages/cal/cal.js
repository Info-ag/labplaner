const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function daysInMonth (month, year) {
    return new Date(year, month, 0).getDate();
}


//month from 0-11
function buildBasis(month, year, size, anker){
    var div1 = $("<div></div>").addClass("calendar");
    if(size = true){
        div1.addClass("calendar-lg");
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
    console.log(prevAndNextMonth);
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
    divBody = generateDays(year, month, anker, divBody);


    divContainer.append(divHeader, divBody);
    div1.append(divNav, divContainer);

    $("#" + anker).append(div1);
}

buildBasis(4, 2018, true, "calendar-anker");
/*
function showAnotherMonth(year, month, anker){
    var divBody = $(anker + "-body");
    divBody.empty();
    divBody = generateDays(year, month, anker, divBody);
    var prevAndNextMonth = getPrevAndNextMonth(year, month); 
    //$(anker + "-left").on("click", showAnotherMonth(prevAndNextMonth.previous.year, prevAndNextMonth.previous.month, anker));
    //$(anker + "-right").on("click", showAnotherMonth(prevAndNextMonth.next.year, prevAndNextMonth.next.month, anker));
    //$(anker + "-left").click(showAnotherMonth(prevAndNextMonth.previous.year, prevAndNextMonth.previous.month, anker));
    //$(anker + "-right").click(showAnotherMonth(prevAndNextMonth.next.year, prevAndNextMonth.next.month, anker));

}*/

function showAnotherMonth(event){
    anker = event.data.anker;
    month = event.data.month;
    year = event.data.year;
    console.log(event.data);
    var divBody = $("#" + anker + "-body");
    divBody.empty();
    var prevAndNextMonth = getPrevAndNextMonth(year, month); 
    $("#" + anker + "-heading").text(monthNames[month] + " " +  year);
    $("#" + anker + "-right").off("click");
    $("#" + anker + "-left").off("click");
    $("#" + anker + "-left").click({"year": prevAndNextMonth.previous.year, "month": prevAndNextMonth.previous.month, "anker": anker }, showAnotherMonth)
    $("#" + anker + "-right").click({"year": prevAndNextMonth.next.year, "month": prevAndNextMonth.next.month, "anker": anker }, showAnotherMonth)
    divBody = generateDays(year, month, anker, divBody);

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


function generateDays(year, month, anker, divBody){
    firstWeekDay = new Date(year, month).getDay();
    console.log(firstWeekDay);
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




function buildPrevDay(day){
    div = $("<div></div>").addClass("calendar-date prev-month disabled");
    button = $("<button></button>").addClass("date-item").text(day.getDate());
    div.append(button);
    return div;
};

function buildCurrentDay(day){
    div = $("<div></div>").addClass("calendar-date current-month");
    button = $("<button></button>").addClass("date-item").text(day.getDate());
    div.append(button);
    return div;
}

function buildNextDay(day){
    div = $("<div></div>").addClass("calendar-date next-month disabled");
    button = $("<button></button>").addClass("date-item").text(day.getDate());
    div.append(button);
    return div;
}
