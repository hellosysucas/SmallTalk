var nowFriend = "";
var myself = "";
var oldStore = "";
var selectedStore = "";
//var dir_comment = {'storeName':'','userName':'','page':0};
$(function(){
    $("#modal-header").css("display","none");
    if ($("#myself").html()){
        myself = nowFriend = $("#myself").html();
        $("#myself").css("background-color","#eeeeee");
        getUserCommentMessage(myself,0);
    }
    else{
        $.post("../getStoreMessage/",{'store':oldStore,'page':0},function(data){
            $("#showComments").html(data);
        });
    }
    updateStoreList(0);
    $('#wrongStoreName').css('color','red');
    $('#wrongPlace').css('color','red');
})

function getUserCommentMessage(uid,page){
    $.post("../friends/message/",{'username':uid,'page':page},function(data){
		$("#showComments").html(data);
	});
}

function showMessage(event){
    //$("#showUserMessage").html(friend);
    if (oldStore.length > 0){
        $("#"+oldStore).css("background-color","");
        oldStore = '';
    }
    if (nowFriend.length > 0){
        $("#"+nowFriend).css("background-color","");
    }
    if (nowFriend == myself)
        $("#myself").css("background-color","");
    friend = event.id;

    $("#"+friend).css("background-color","#eeeeee");
    
    if (friend == myself)
        $("#myself").css("background-color","#eeeeee");
    nowFriend = friend;
    
    getUserCommentMessage(friend,0);
}

function deleteFriend(event){
    nowFriend = event.id;
    $.post("../friends/deleteFriend",{'username':nowFriend},function(data){
        if ( !data )
            window.open("../","_self");
    });
    window.open("../friends/","_self");
}

function showStoreMessage(event){
    id = event.id;
    
    $("#"+id).css("background-color","#eeeeee");
    if (nowFriend == myself)
        $("#myself").css("background-color","");
    if (nowFriend.length > 0){
        $("#"+nowFriend).css("background-color","");
        nowFriend = '';
    }
    if (oldStore != "")
        $("#"+oldStore).css("background-color","");
        
    oldStore = id;
    $.post("../getStoreMessage/",{'store':oldStore,'page':0},function(data){
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

//用于弹出框中的搜索框
function searchStore(){
	storeName = $('#storeName').val();
	if (check_uname(storeName,'wrongChar')){
		//判断商店是否存在
        $.post('../is_store_exist/',{'store':storeName},function(data){
            if (data.length > 0){
                $("#showStoreList").html(data);
            }
            else
                $('#wrongChar1').html("商店不存在！您可以为此创建一个新的商店！");
        });
	}
}

//添加一个新的商铺
function makeSubmit(){
    $('#wrongChar').html();
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

//为0代表往前跳转，即页面数字减小；为1为往后跳转，页面数字加大
function changePageList(p1,p2){
    id = '';
    if (p1 == '1'){
        id ='#a_';
    }
    else if (p1 == '0'){
        id = '#b_';
    }
    else if (p1 == '2'){
        id = '#c_';
    }
    
    if (p2 == '1') {
        for ( i = 1; i <= 5; i++) {
            $(id + i).html(parseInt($(id + i).html()) + 5);
        }
    } else if (p2 == '0') {
        temp = parseInt($(id+'1').html());
        if (temp == 0)
            return false;
        else if (temp > 5) {
            for ( i = 1; i <= 5; i++) {
                $(id + i).html(parseInt($(id + i).html()) - 5);
            }
        }
    }

    return false;
}

//更改显示内容
function changeStoreList(event,p){
    id = event.id;
    page = parseInt($('#'+id).html()) - 1;
    if (p == 1){
        updateStoreList(page-1);
    }
    else if (p == 0){
        if (nowFriend.length > 0){
            getUserCommentMessage(nowFriend,page);
        }
        else{
            $.post("../getStoreMessage/",{'store':oldStore,'page':page},function(data){
                $("#showComments").html(data);
            });
        }
    }
}

//搜索好友
function searchFriend(){
    userName = $('#userName').val();
    if (check_uname(userName,'wrongChar')){
        $.post('../searchFriend/',{'username':userName},function(data){
            if (data.length > 0)
                $("#showFL").html(data);
            else
                $("#wrongChar").html("输入的用户名不是您的好友！");
        });
    }
}

//更新好友列表
function changeFriendsList(event){
    id = event.id;
    page = parseInt($("#"+id).html()) - 1;
    $.post('../changeFriendsList/',{'page':page},function(data){
        if (data.length > 0)
            $("#showFL").html(data);
        else
            $("#showFL").html("您尚未添加任何好友！");

    });
}

function changeShopState(event){
    text = event.id;
    text = text.split('_');
    oldStore = shopName = text[0];
    content = text[1];
    nowFriend = "";
    $.post('../changeShopState/',{'store':shopName,'content':content},function(data){
        $('#showShopComments').html(data);
    });
}

function changeSituation(event){
    id = event.id;
    text = $('#'+id).html();
    temp = text;
    $('#'+id).html($('#Sa').html());
    $('#Sa').html(temp);
}

function beFriend(event){
    id = event.id;
    friendName = (id.split('_'))[0];
    $.post('../beFriend/',{'username':friendName},function(data){
        $('#'+id).html(data);
    });
}
