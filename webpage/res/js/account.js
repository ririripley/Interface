
$(function ()
{

    // Set title and selected nav-bar item
    $("body").css({"min-width": "1100px"});''
    $("#nav_add").addClass("active");

}
);
/*...........open change window...................*/
 jQuery(document).ready(function($) {
  $('.change').click(function(){
    $('.theme-popover-mask').fadeIn(100);
    $('.theme-popover').slideDown(200);
  })

/*...........close change window...................*/
  $('.btn-close, .theme-poptit .close').click(function(){
    $('.theme-popover-mask').fadeOut(100);
    $('.theme-popover').slideUp(200);
  })


  


  /*...........save change...................*/
$("#submit").click(function(){
  var first_name=$('#firstname').val();
  var last_name=$('#lastname').val();
  var email=$('#email').val();
  var school=$('#school').val();

 // Validate all fields
    if (!$("#firstname").val() || parseInt($("#firstname").val()) < 0)
    {
        alert("Please fill in the first name!");
        return false;
    }
    if (!$("#lastname").val() || parseInt($("#lastname").val()) < 0)
    {
        alert("Please fill in the last name!");
        return false;
    }
    if (!$("#email").val() || parseInt($("#email").val()) < 0)
    {
        alert("Please fill in the email!");
        return false;
    }

// 分成三个reset：
   // 1)
    // api/reset-password
    // 用户填写：
    // original_password 原来的密码
    // password1 修改后的密码
    // password2  再填一次修改后的密码
    // 原密码等于旧密码        diff_original：false,
    // 两次输的密码不一致 password1 != password2     confirm_new：false
    //diff_original和confirm_new都为true, reset_password才为true
    // HZJ 返回的值 return jsonify({"reset_password": True, "diff_original":True, "confirm_new":True})

    //2)
    // api/reset-username
    // api/reset-username
    // 用户填写：
    // new_username 修改后的username
    // 如果原来的username 和 修改后的username 一样，
    // HZJ 返回的值  return jsonify({"reset_username": False})


    //3)

     // /api/reset-email
    // 用户填写：
    // password
    // new_email
    // 密码错误 ： confirm: false
   //修改的email已被used : new_mail: false
    //new_mail和confirm都为true, reset_email才为true
    // HZJ 返回的值 return jsonify({"reset_email": False,"new_mail": false,"confirm": false })

  $.ajax({
    type: "post",
    url: "http://localhost:3000/api/reset",
    dataType: "json",
      // from JXY to me
    data:{ first_name: first_name, last_name: last_name, email:email, school:school},
    success: function(data){
          alert('Modify successfully!');
        }
  });
  /*
  console.log({ first_name: first_name, last_name: last_name, email:email, school:school });
  return false
  });*/

})


