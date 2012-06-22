
var identity_prompt = "电子邮箱/手机号";

function signin(identity, password, onSuccess, onFailure) {
  $.get("/rsa/public.key", function(result) {
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
      success: function(data) {
        $.cookies.set("identity", identity);
        $.cookies.set("token", data);
        onSuccess(data);
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
});
