var login = document.getElementById('my_captcha_form');
                login.addEventListener("click", function (evt) {
                    var response = grecaptcha.getResponse();
                    if (response.length == 0) {
                        //reCaptcha  verified
                        Swal.fire("", "please verify the captcha!", "warning");
                        evt.preventDefault();
                        return false;
                    }
                });

                function show_hide_password(target){
                    var input = document.getElementById('password');
                    if (input.getAttribute('type') == 'password') {
                        target.classList.add('view');
                        input.setAttribute('type', 'text');
                    } else {
                        target.classList.remove('view');
                        input.setAttribute('type', 'password');
                    }
                    return false;
                }
                

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

  togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});
