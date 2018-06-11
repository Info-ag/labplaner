var descriptionInput = $("#description");
var displayNameInput = $("#displayname");

var nameButton = $("#submit-name");
var descriptionButton = $("#submit-description");

id = $("#ag-id").val();

nameButton.on("click", function () {
    if (document.getElementById("displayname").checkValidity()) {
        var data = {"display_name": displayNameInput.val()};
        submit(data);
    }
});

descriptionButton.on("click", function () {
    if (document.getElementById("description").checkValidity()) {
        var data = {"description": descriptionInput.val()};
        submit(data);
    }
});

function submit(data) {
    $.ajax({
        type: 'PUT',
        url: changeValuesUrl + id,
        data: data,
        dataType: "json",
        cache: false,
        beforeSend: function () {
            nameButton.addClass("is-loading");
            descriptionButton.addClass("is-loading");
        }
    }).done(function () {
        location.reload();
    });
}
