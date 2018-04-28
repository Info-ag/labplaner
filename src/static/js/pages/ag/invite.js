Array.prototype.contains = function (needle) {
    for (var i in this) {
        if (this[i] === needle) return true;
    }
    return false;
}

Array.prototype.removeObject = function (needle) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] === needle) {
            this.splice(i, 1);
            return true;
        }
    }
    return false;
}
var hasSuggestion = false;
var users = Array();

var usernameInput = $("#usernameInput");
var timeoutLength = 500;
var timeout;

usernameInput.on("input", function () {
    timeout = setTimeout(function () {
        hasSuggestion = false;
        if (!usernameInput.val()) {
            $("#menu-anker").hide();
            return;
        }
        $.ajax({
            type: 'GET',
            url: '/api/v1/user/?query=' + usernameInput.val() + "&count=5",
            data: "{}",
            dataType: "json",
            cache: false,
            beforeSend: function () {
                $("#input-loading").show();
            }
        }).done(function (response) {
            $("#input-loading").hide();
            $("#menu-anker").empty();
            $("#menu-anker").show();
            var objCount = 0;
            for (let i in response) {
                if (!response[i].hasOwnProperty("username") || users.contains(response[i].username)) {
                    continue;
                }
                objCount++;
                var menuItem = $("<li></li>").addClass("menu-item");
                var aTag = $("<a></a>").attr("href", "#").on("click", function () {
                    addUser(response[i]);
                });
                var div1 = $("<div></div>").addClass("tile tile-centered");
                var div2 = $("<div></div>").addClass("tile-icon");
                var img = $("<img/>").addClass("avatar avatar-sm").attr("alt", response[i].username).attr("src", response[i].picture);
                var div3 = $("<div></div>").addClass("tile-content").text(response[i].username);
                menuItem.append(aTag);
                aTag.append(div1);
                div1.append(div2);
                div2.append(img);
                div1.append(div3);
                $("#menu-anker").append(menuItem);
            }
            if (!objCount) {
                showEmpty();
            }else{
                hasSuggestion = true;
            }
        });
    }, timeoutLength);
});

function showEmpty() {
    var menuItem = $("<li></li>").addClass("menu-item");
    var aTag = $("<a></a>").attr("href", "#");
    var div1 = $("<div></div>").addClass("tile tile-centered");
    var div3 = $("<div></div>").addClass("tile-content").text("Keine Nutzer mit übereinstimmenden Namen gefunden");
    menuItem.append(aTag);
    aTag.append(div1);
    div1.append(div3);
    $("#menu-anker").append(menuItem);
    hasSuggestion = false;
}

function addUser(user) {
    users.push(user.username);
    usernameInput.parent().removeClass("is-error");
    var div = $("<div></div>").addClass("chip");
    div.attr("data-username", user.username);
    var img = $("<img/>").addClass("avatar avatar-sm").attr("alt", user.username).attr("src", user.picture);
    var a = $("<a></a>").addClass("btn btn-clear").attr("href", "#").attr("aria-label", "Close").attr("role", "button");
    a.on("click", function () {
        div.remove();
        users.removeObject(user.username);
    });
    div.text(user.username);
    div.append(a);
    div.prepend(img);
    div.insertBefore(usernameInput);

    usernameInput.val("");
    $("#menu-anker").hide();
    hasSuggestion = false;
    usernameInput.focus()
}

usernameInput.on("keydown", function (e) {
    if (!usernameInput.val() && e.keyCode === 8) {
        $(".form-autocomplete-input").find(".chip").last().find("a").click();
    }
});

var inviteForm = $("#invite-form");
inviteForm.submit(function (event) {
    event.preventDefault();
    if (users.length === 0) {
        usernameInput.parent().addClass("is-error");
        return;
    }
    $.ajax({
        type: 'POST',
        url: $(inviteForm).attr('action'),
        data: {users: users},
        dataType: "json",
        cache: false,
        beforeSend: function () {
            $("#menu-anker").hide();
            $("#invite").addClass("loading");
            return true;
        }
    }).done(function (response) {
        window.location.href = response.redirect;
    });

});


$(document).keydown(function(e) {
    if($("#usernameInput, #menu-anker > .menu-item > a").is(":focus") && hasSuggestion){
        switch(e.which) {
            case 38: //left 
            if(document.activeElement.nodeName == "INPUT"){
                $("#menu-anker > .menu-item").last().children().first().focus();
            }else if(document.activeElement.nodeName == "A"){
                if($(document.activeElement).parent().prev().length != 0){
                    $(document.activeElement).parent().prev().children().first().focus();
                }else{
                    $(document.activeElement).parent().parent().first().children().last().children().first().focus();
                }   
            }else{
                return;
            }
            break;

            case 40: // right
            console.log(document.activeElement.nodeName);
            if(document.activeElement.nodeName == "INPUT"){
                $("#menu-anker > .menu-item").first().children().first().focus();
            }else if(document.activeElement.nodeName == "A"){
                if($(document.activeElement).parent().next().length != 0){
                    $(document.activeElement).parent().next().children().first().focus();
                }else{
                    $(document.activeElement).parent().parent().first().children().first().children().first().focus();
                }   
            }else{
                return;
            }
            break;

            default: return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    }
});