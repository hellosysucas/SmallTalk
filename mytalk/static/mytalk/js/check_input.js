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
        $('#' + message_container_id).html("请输入合法邮箱");
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
    
function check_login(){
    var username = $("#username").val();
    var password = $("#password").val();
    var is_username_ok = check_uname(username,"wrongChar");
    var is_password_ok = false;
    if (password.length > 0)
        is_password_ok = true;
    else
        $("#wrongPassword").html("密码为空");
    if (is_username_ok && is_password_ok){
        password = CryptoJS.SHA1(password)+"";
        $.post("../detectLogin/",{'username':username,'password':password},
            function(data){
                if (data == "false")
                    $("#showError").html("用户名或密码有误，请输入合法用户名或密码！若未注册，请先注册！");
                else
                    window.open("../","_self");
            }
        );
    }
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

function check_register(){
    var username = $("#username").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var updatePassword = $("#updatePassword").val();
    
    var is_username_ok = check_uname(username,"wrongChar");
    var is_email_ok = check_email(email,"wrongEmail");
    var is_password_ok = true;
    if ( password.length == 0 ){
        is_password_ok = false;
        $("#wrongPassword").html("密码为空");
    }
    else if ( updatePassword.length == 0 ){
        is_password_ok = false;
        $("#wrongUpdatePassword").html("确认密码为空");
    }
    else if (password != updatePassword){
		is_password_ok = false;
        $("#wrongPassword").html("密码不一致");
        $("#wrongUpdatePassword").html("密码不一致");
    }
	
	if (is_username_ok && is_email_ok && is_password_ok){
        //alert(CryptoJS.SHA1(password));
        password = CryptoJS.SHA1(password)+"";

		$.post("../register/doRegister/",
                {'username':username,'email':email,'password':password},
                function(data){
                    if (data == "true")
                        window.open("../","_self");
                    else if (data == "false")
                        check_register();
                    else
                        $("#showError").html(data);
                }
        );
	}
}

function operation_exit(){
    $.post("../exitOperation/",{},function(data){
        if (data == "true")
            window.open("../","_self");
    });
}