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




var inputQuantity = [];
    $(function() {     
      $(".zipcode-number").on("keyup", function (e) {
        var $field = $(this),
            val=this.value,
            $thisIndex=parseInt($field.data("idx"),11); 
        if (this.validity && this.validity.badInput || isNaN(val) || $field.is(":invalid") ) {
            this.value = inputQuantity[$thisIndex];
            return;
        } 
        if (val.length > Number($field.attr("maxlength"))) {
          val=val.slice(0, 10);
          $field.val(val);
        }
        inputQuantity[$thisIndex]=val;
      });      
    });
