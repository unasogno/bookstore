function begin_login(dialog, onSuccess, onFailure) {
  var closable = false;
  $(dialog)
    .load("/bookhub/login.html")
    .dialog({
      height: 200,
      buttons: {
        "登录": function() {
          var identity = $("#login_identity").val();
          var password = $("#login_password").val();
          signin(identity, password, 
            function(data) {
              closable = true;
              $(dialog).dialog("close");
              onSuccess(data);
            },
            function(status, error){
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

