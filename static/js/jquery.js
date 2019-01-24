$(document).ready(function () {
    $("#about-btn").addClass('btn btn-success')
    $("#about-btn").click(function (event) {
        alert("You clicked on The button using JQuery !");
    });
    $(".ouch").click(function (event) {
        alert("You clicked me! ouch!");
    });
    $("p").hover(function () {
        $(this).css('color', 'red');
    }, function () {
        $(this).css('color', 'blue');
    });
    $("#about-btn").click(function (event){
        msgstr=$("#msg").html()
        msgstr=msgstr+"  OOOOOO"
        $("#msg").html(msgstr)
    });
});
