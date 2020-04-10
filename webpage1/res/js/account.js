
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
  


  $.ajax({
    type: "post",
    url: "http://localhost:3000/login",
    dataType: "json",
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


