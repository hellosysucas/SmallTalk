var nowFriend = "";
var myself = "";
var oldStore = "";
var selectedStore = "";
$(function(){
    $("#modal-header").css("display","none");
    if ($("#myself").html()){
        myself = nowFriend = $("#myself").html();
        $("#myself").css("background-color","#eeeeee");
        getUserCommentMessage(myself);
    }
    else{
        $.post("../getStoreMessage/",{'store':oldStore},function(data){
            $("#showComments").html(data);
        });
    }
    updateStoreList(0);
    $('#wrongStoreName').css('color','red');
    $('#wrongPlace').css('color','red');
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

function addStore(){
    if ($("#myself").html()){
        $("#modal-header").css("display","");
    }
    else
        $('#wrongChar').html("请先<a href='../signIn/'>登录</a>或<a href='../register/'>注册</a>");
}

function cutInput(){
    $("#modal-header").css("display","none");
    $('#wrongChar').html("");
    updateStoreList(0);
    return true;
}

function setSelectedStore(event){
    id = event.id;
    selectedStore  = $("#"+id).html();
}

function updateStoreList(whichPage){
    $.post("../getStoreList/",{'page':whichPage},function(data){
        $("#showStoreList").html(data);
    });
}

function makeSureSelectedStore(){
    if (selectedStore != ""){
        $('#selectedStore').html(selectedStore);
        $('#myModal').modal('hide');
    }
    selectedStore = '';
}

//改变标签状态，即点击好友圈时，替换公共
function changeState(){
    temp = $("#Fa").html();
    $("#Fa").html($("#Fb").html());
    $("#Fb").html(temp);
}

function searchStore(){
	storeName = $('#storeName').val();
	if (check_uname(storeName,'wrongChar')){
		//判断商店是否存在
        $.post('../is_store_exist/',{'store':storeName},function(data){
            if (data.length > 0){
                $("#showStoreList").html(data);
            }
            else
                $('#wrongChar').html("商店不存在！您可以为此创建一个新的商店！");
        });
	}
}

function makeSubmit(){
    storeName = $('.storeName').val();
    storePlace = $('.storePlace').val();

    $.post('../is_store_exist/',{'store':storeName},function(data){
        if (data.length > 0){
        $('#wrongChar').html("您输入的商店已经存在！");
        $('#showStoreList').html(data);
        $("#modal-header").css("display","none");
        }
        else{
            if (check_uname(storeName,'wrongStoreName') && check_uname(storePlace,'wrongPlace')){
                $.post('../insert_new_store/',{'storeName':storeName,'storePlace':storePlace},function(data){
                    if (data.length > 0){
                        $('#showStoreList').html(data);
                    }
                    else
                        $('#wrongChar').html("商店名或地点名不合法，或商店名已存在！");
                });
                $("#modal-header").css("display","none");
            }
        }
    });
}

//提交评论，获得评论内容，商店名称，以及可见性，为1代表公共可见，为0代表好友可见
function commentSubmit(){
    text = $('#inputComment').val();
    if (myself == ""){
        $('#inputComment').val(text + "\n\n请先登录，或注册！")
        return;
    }
    visibility = 1;
    temp = $('#Fb').html();
    if (temp == "好友圈")
        visibility = 0;
    store = $('#selectedStore').html();
    
    note = text+'\n';
    is_ok = true;
    
    if (store == "选择点评商户"){
        is_ok = false;
        note += "请选择一个商户, ";
    }
    
    if (text == ""){
        is_ok = false;
        note += "请输入评论信息";
    }
    
    if (!is_ok)
        $('#inputComment').val(note);
    else{
        $.post('../insert_new_comment/',{'store':store,'comment':text,'visibility':visibility},function(data){
            if (data.length > 0)
                $('#showComments').html(data);
            else
                note += "\n\n信息插入失败！";
        });
    }
}