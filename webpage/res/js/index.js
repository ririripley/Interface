$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});


$('.primary-blue-button').click(function(){
    $('#gray').show();
    $('#form').show();//查找ID为form的DIV show()显示#gray
    tc_center();
  });
  //点击关闭按钮
  $('a.close_button').click(function(){
    $('#gray').hide();
    $('#form').hide();//查找ID为form的DIV hide()隐藏
  })

  //窗口水平居中
  $(window).resize(function(){
    tc_center();
  });

  

  function tc_center(){
    var _top=($(window).height()-$('.form').height())/2-10;
    var _left=($(window).width()-$('.form').width())/2;
    
    $('.form').css({top:_top,left:_left});
  } 
  

/*...........Login in...................*/
$("#login_submit").click(function(){
  var login_email=$('#login_email').val();
  var password=$('#password').val();
  //check the format of login_email address and password
  //........
  //send ajax request 使用post方式发送json字符串给后台login
  
  $.ajax({
    type: "post",
    url: "http://localhost:5000/api/login",
    // HZJ: /api/login
    dataType: "json",

    // jxy to me:
    data:{ login_email: login_email, password: password },

      // data: to JXY
    // HZJ :return jsonify({"login": True})

//此处function需要修改
    success: function(data){
alert('Wrong usrname or password! Please enter again');

    //接受返回的数据，前端判断采取的动作


     if(data){
     if(data == "true"){
          alert('Wrong usrname or password! Please enter again');
          //window.location.href="login";
        }else{
          alert('Login in successfully!');
          window.location.href="JMT";
        }
     }
    else{
     }

    }
  });
  
  /*console.log({ login_email: login_email, password: password });
  return false;*/
});

/*...........register...................*/
$("#register_submit").click(function(){
  var first_name=$('#first_name').val();
  var last_name=$('#last_name').val();
  var register_email=$('#register_email').val();
  var set_password=$('#set_password').val();

  $.ajax({
    type: "post",
    url: "http://localhost:5000/api/register",
//HZJ: api/register
    dataType: "json",

      //此处只需要username 即可，对数据库会更方便 去掉first_name 和 last_name 用username 代替
      // 即改为使用三个变量username, register_email, set_password
    data:{  first_name:first_name,
            last_name:last_name,
            register_email: register_email, 
            set_password: set_password 
          },
// HZJ 返回的数据为
// return jsonify({'register': False, 'register_email':True, 'username':False})
      // register_email或者username已用，则会返回false , 两者中任何一个为false， register都为false
    success: function(data){
    //接受返回的数据，前端判断采取的动作
      if(data){
        if(data.message=="false"){
          alert('This email has already registed');
          //window.location.href="login";
        }else{
          alert('regist successfully!');
          window.location.href="JMT";
        }
      } else{
      }
    }
  });
  
  /*
  console.log({first_name:first_name, 
            last_name:last_name,
            register_email: register_email, 
            set_password: set_password  });
  return false;*/


    /**
     * 还需要添加的button:
     * URL : /api/logout
     * HZJ RETURN: return jsonify({"logout": True})
     */
});

