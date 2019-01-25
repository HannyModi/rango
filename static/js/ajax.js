$('#likes').click(function () {
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like/', { category_id: catid }, function (data) {
        $('#like_count').html(data);
        $('#likes').hide();
    });
});

$("#suggestion").keyup(function () {
    var query;
    query = $(this).val();
    $.get('/rango/suggest/', { suggestion: query }, function (data) {
        $("#cats").html(data);
    });
});

$(".rango-add").click(function () {
    var catid, title, url;
    catid = $(this).attr("data-catid");
    title=$(this).attr("data-title");
    url=$(this).attr("data-url");
    me=$(this);
    $.get('/rango/add/',{categoryid:catid,title:title,url:url},function(data){
        $('#pages').html(data);
        me.hide();
    });
});
