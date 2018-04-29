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
    var btnLeft = $("<button></button>").addClass("btn btn-action btn-link btn-lg");
    var iBtnLeft = $("<i></i>").addClass("icon icon-arrow-left");
    btnLeft.append(iBtnLeft);
    var divMonth = $("<div></div>").addClass("navbar-primary").text(monthNames[month] + " " +  year);
    var btnRight = $("<button></button>").addClass("btn btn-action btn-link btn-lg");
    var iBtnRight = $("<i></i>").addClass("icon icon-arrow-right");
    btnRight.append(iBtnRight);
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
    var divBody = $("<div></div>").addClass("calendar-body");
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
    console.log(daysInPrevMonth);
    for( var i = ( - daysInPrevMonth) + 1 ; i <= 0; i++){
        var divDay = buildPrevDay(new Date(year, month, i));
        divBody.append(divDay);
        console.log(i);
    }

    lastDay = new Date(year, (month+1), 0);
    var lastDayNumber = lastDay.getDate();
    console.log(lastDayNumber);
    for (var i = 1; i <= lastDayNumber; i++){
        var divDay = buildCurrentDay(new Date(year, month, i));
        divBody.append(divDay);
        console.log(divDay);
    }
    lastWeekDay = lastDay.getDay();
    var daysInNextMonth = 7 - lastWeekDay;
    console.log(daysInNextMonth);
    for (var i = 1; i <= daysInNextMonth; i++){
        var divDay = buildNextDay(new Date(year, (month + 1), i));
        divBody.append(divDay);
    }
    divContainer.append(divHeader, divBody);
    div1.append(divNav, divContainer);



    $(anker).append(div1);
}

buildBasis(4, 2018, true, "#calendar-anker");

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
