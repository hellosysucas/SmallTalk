function check_uname(uname, message_container_id){
	var asc=' 	~`!@#$%^&*()_-+=|\{}[]:;<>,.?/';
	asc+='""';
	asc+="''";
	asc+="~·……——|、￥#@《》，。、“”‘’{}【】、、？.";

	$('#'+message_container_id).html("");

	if( uname.length == 0 ){
		$('#'+ message_container_id).html("输入为空");	
		return false;
	}

	var flag = true;
	for( var i = 0; i < uname.length; ++i){
		var ch = uname.charAt(i);
		if( asc.indexOf( ch ) > -1 ){
			flag = false;
			break;	
		}	
	}
	
	if( flag == false ){
		$('#' + message_container_id).html("请输入 字符，数字,或 中文");
	}
	return flag;
}

function check_email(email,message_container_id){
    $('#' + message_container_id).html("");
    if (email.length == 0){
        $('#'+ message_container_id).html("输入为空");	
		return false;
    }
    
    var flag = true;
    if (email.indexOf(".")==-1 || email.indexOf("@")==-1 || email.indexOf("com")==-1){
        flag = false;
        $('#' + message_container_id).html("请输入合法邮箱"+email+"  "+email.indexOf(".")+email.indexOf("@")+email.indexOf("com"));
    }
    else
        $('#'+ message_container_id).html("");
    return flag;
}

function check_login_password(password,message_container_id){
    $('#' + message_container_id).html("");
    if (password.length == 0){
        $('#'+ message_container_id).html("密码输入为空");	
		return false;
    }
    $('#'+ message_container_id).html("");
    return true;
}

function check_update_password(updatePassword,message_container_id){
    $('#'+ message_container_id).html("");
    password = $('#password').val();
    if (password != updatePassword){
        $('#'+ message_container_id).html("密码不合法");
        return false;
    }
    return true;
}