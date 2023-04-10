
function show_hide_password(target){
	var input = document.getElementById('password-input');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}


function show_hide_password_sign(target){
	var input = document.getElementById('txtNewPassword');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}

function show_hide_password_confirm(target){
	var input = document.getElementById('password-input');
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
}



var state= false;
function toggle(){
    if(state){
	document.getElementById("password").setAttribute("type","password");
	document.getElementById("eye").style.color='#7a797e';
	state = false;
     }
     else{
	document.getElementById("password").setAttribute("type","text");
	document.getElementById("eye").style.color='#5887ef';
	state = true;
     }
}




// function verifyPassword() {
// 	var pw = document.getElementById("pswd").value;
// 	var pw1 = document.getElementById("pswd1").value;  
// 	//check empty password field
// 	if(pw == "") {
// 	   document.getElementById("message").innerHTML = "**Fill the password please!";
// 	   return false;
// 	}

// 	if(pw != pw1)  
// 	{   
// 	  //alert("Passwords did not match");  
// 	  document.getElementById("message1").innerHTML = "Passwords did not match";
// 	  return false;
// 	}
// 	else {  
// 		//alert("Password created successfully");  
// 	  }  
   
//    //minimum password length validation
// 	if(pw.length < 8) {
// 	   document.getElementById("message").innerHTML = "**Please type at least 8 charcters";
	   
// 	   return false;
// 	}

	
//   //maximum length of password validation
// 	if(pw.length > 15) {
// 	   document.getElementById("message").innerHTML = "**Password length must not exceed 15 characters";
// 	   return false;
// 	} else {
// 	   alert("Password is correct");
// 	}
//   }

/*global $, document, window, setTimeout, navigator, console, location*/
  $(document).ready(function () {
      
    'use strict';
    
    var usernameError = true,
      emailError    = true,
      passwordError = true,
      passConfirm   = true;
    
    
    // Form validation
    $('input').blur(function () {
    
      
      // PassWord
      if ($(this).hasClass('pass')) {
          if ($(this).val().length < 8) {
              $(this).siblings('span.error').text('Please type at least 8 charcters').fadeIn().parent('.form-group').addClass('hasError');
              passwordError = true;
          } else {
              $(this).siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
              passwordError = false;
          }
      }
     
    });


   
    $('input').blur(function () {            
        
    // PassWord confirmation
    if ($('.pass').val() !== $('.passConfirm').val()) {
        $('.passConfirm').siblings('.error').text('Passwords don\'t match').fadeIn().parent('.form-group').addClass('hasError');
        passConfirm = false;
    } else {
        $('.passConfirm').siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
        passConfirm = false;
    }
   
  });
    
    });


    const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#txtNewPassword');

  togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});


const togglePassword_con = document.querySelector('#togglePassword_con');
const password2 = document.querySelector('#password-input');

togglePassword_con.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
    password2.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});
