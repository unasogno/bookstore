
var identity_prompt = "电子邮箱/手机号";

function signin(identity, password, onSuccess, onFailure) {
  $.get("/rsa/public.pem", function(result) {
    var pub = result;
    var pubkey = new RSAKey();
    pubkey.setPublic(pub, '10001');
    identity = pubkey.encrypt(identity);
    password = pubkey.encrypt(password);

    $.ajax({
      url:"/api/signin", 
      data: {"identity": identity,
             "password": password
      }, 
      success: function(token) {
        onSuccess(token);
      },
      error: function(jqXHR, status, exception) {
        onFailure(jqXHR.status, exception);
      }
    });
  });
}

$(document).ready(function (){
  $(login_identity).val(identity_prompt);

  $(login_identity).focus(function(){
    var identity = $(login_identity).val();
    if (identity == identity_prompt) {
      $(login_identity).val("");
    }
  });

  $(login_identity).blur(function(){
    var identity = $(login_identity).val();
    if (identity == "") {
      $(login_identity).val(identity_prompt);
    }
  });
});
