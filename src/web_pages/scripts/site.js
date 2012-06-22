function login(dialog, success, failure) {
  $(dialog)
    .load("/bookhub/login.html")
    .dialog({
      height: 200,
      buttons: {
        "登录": function() {
          var identity = $("#login_identity").val();
          var password = $("#login_password").val();
          signin(identity, password);
        },
        "清除": function() {
          $("#login_identity").val("");
          $("#login_password").val("");
        }
      },
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return false;
      }
    });

  $(dialog).dialog("open");
}

function signin(identity, password) {
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
        alert(data);
      },
      error: function(jqXHR, status, exception) {
        alert(exception);
      }
    });
  });
}
