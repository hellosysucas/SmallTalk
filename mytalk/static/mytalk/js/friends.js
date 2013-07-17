var nowFriend = "";
var myself = "";
$(function(){
    myself = nowFriend = $("#myself").val();
    $("#"+nowFriend).css("background-color","yellow");
    $("#myself").css("background-color","yellow");
    getMessage(myself);
})

function getMessage(uid){
    $.post("../friends/message/",{'username':uid},function(data){
		$("#showUserMessage").html(data);
	});
}

function showMessage(friend){
    $("#showUserMessage").html(friend);
    $("#"+nowFriend).css("background-color","white");
    if (nowFriend == myself)
        $("#myself").css("background-color","white");
    $("#"+friend).css("background-color","yellow");
    
    if (friend == myself)
        $("#myself").css("background-color","yellow");
    nowFriend = friend;
    
    getMessage(friend);
}

function deleteFriend(){
    $.post("../friends/deleteFriend",{'username':nowFriend},function(data){
        if ( !data )
            window.open("../","_self");
    });
    window.open("../friends/","_self");
}