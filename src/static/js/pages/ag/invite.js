var usernameInput = $("#usernameInput");
var timeoutLength = 500;
var timeout;

usernameInput.on("input", function () {
    timeout = setTimeout(function () {
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
            if (response.length != 0) {

                for (let i in response) {

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


            } else {
                var menuItem = $("<li></li>").addClass("menu-item");
                var aTag = $("<a></a>").attr("href", "#");
                var div1 = $("<div></div>").addClass("tile tile-centered");
                var div3 = $("<div></div>").addClass("tile-content").text("Keine Nutzer mit übereinstimmenden Namen gefunden");
                menuItem.append(aTag);
                aTag.append(div1);
                div1.append(div3);
                $("#menu-anker").append(menuItem);
            }
        });
    }, timeoutLength);
});


function addUser(user) {
    var div = $("<div></div>").addClass("chip");
    var img = $("<img></img>").addClass("avatar avatar-sm").attr("alt", user.username).attr("src", user.picture);
    var a = $("<a></a>").addClass("btn btn-clear").attr("href", "#").attr("aria-label", "Close").attr("role", "button");
    a.on("click", function () {
        div.remove();
    });
    div.text(user.username);
    div.append(a);
    div.prepend(img);
    div.insertBefore(usernameInput);

    usernameInput.val("");
    $("#menu-anker").hide();
    usernameInput.focus()
}

usernameInput.on("keydown", function (e) {
    if (!usernameInput.val() && e.keyCode === 8) {
        $(".form-autocomplete-input").find(".chip").last().remove();
    }
});