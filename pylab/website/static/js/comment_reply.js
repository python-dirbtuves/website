$(".comment-reply").click(function () { 
    $(this).css("display", "none");
    $(this).parent().find("form.comment-form").css("display", "block");
});
