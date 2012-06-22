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
            function(data) {
              closable = true;
              $(dialog).dialog("close");
              onSuccess(identity, data);
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

