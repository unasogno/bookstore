function begin_login(dialog, onSuccess, onFailure) {
  var closable = false;
  $(dialog)
    .load("/bookhub/login.html")
    .dialog({
      title: "登录",
      height: 240,
      buttons: {
        "登录": function() {
          var identity = $("#login_identity").val();
          var password = $("#login_password").val();
          signin(identity, password, 
            function(token) {
              closable = true;
              $(dialog).dialog("close");
              identity = $("#login_identity").val();
              //todo: identity should be encrypted for security and consistency.
              $.cookies.set("identity", identity); 
              $.cookies.set("token", token);
              onSuccess(identity, token);
            },
            function(status, error){
              $("#error_info").html("登录失败 － " + status);
              onFailure();
            });
        },
        "清除": function() {
          $("#login_identity").val("");
          $("#login_password").val("");
        }
      },
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return closable;
      }
    });

  $(dialog).dialog("open");
}

