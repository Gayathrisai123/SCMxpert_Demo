window.onload = function () {
    var form = document.getElementById('reservation-form');
    form.button.onclick = function (){
      for(var i=0; i < form.elements.length; i++){
        if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
          Swal.fire('oops! please fill all details');
          return false;
        }
      }
      form.submit();
    }; 
  };


  $('.txtOnly').keypress(function (e) {
    var regex = new RegExp("^[a-zA-Z0-9.,/]");
    // var regex = new RegExp("^[a-zA-Z.,/ $@()]+$");
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }
    else
    {
    e.preventDefault();        
    return false;
    }
});




function spinner() {
	//  SPINNER
	$("#spinner").spinner();
	
	//  INPUT ONLY NUMBERS
	$('#spinner').keyup(function () { 
		 this.value = this.value.replace(/[^0-9]/g,'');
	});
}

// INPUT NUMBER MAX LENGHT
function maxLengthCheck(object) {
	if (object.value.length > object.maxLength)
		object.value = object.value.slice(0, object.maxLength)
}



