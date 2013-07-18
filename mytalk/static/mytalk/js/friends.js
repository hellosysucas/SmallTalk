var nowFriend = "";
var myself = "";
var oldStore = "";
$(function(){
    if ($("#myself").html()){
        myself = nowFriend = $("#myself").html();
        $("#myself").css("background-color","#eeeeee");
        getUserCommentMessage(myself);
    }
})

function getUserCommentMessage(uid){
    $.post("../friends/message/",{'username':uid},function(data){
		$("#showComments").html(data);
	});
}

function showMessage(event){
    //$("#showUserMessage").html(friend);
    $("#"+oldStore).css("background-color","");
    $("#"+nowFriend).css("background-color","");
    if (nowFriend == myself)
        $("#myself").css("background-color","");
    friend = event.id;

    $("#"+friend).css("background-color","#eeeeee");
    
    if (friend == myself)
        $("#myself").css("background-color","#eeeeee");
    nowFriend = friend;
    
    getUserCommentMessage(friend);
}

function deleteFriend(){
    $.post("../friends/deleteFriend",{'username':nowFriend},function(data){
        if ( !data )
            window.open("../","_self");
    });
    window.open("../friends/","_self");
}

function showStoreMessage(event){
    id = event.id;
    
    $("#"+id).css("background-color","#eeeeee");
    $("#"+nowFriend).css("background-color","");
    if (nowFriend == myself)
        $("#myself").css("background-color","");
    if (oldStore != "")
        $("#"+oldStore).css("background-color","");
        
    oldStore = id;
    $.post("../getStoreMessage/",{'store':oldStore},function(data){
        $("#showComments").html(data);
    });
}