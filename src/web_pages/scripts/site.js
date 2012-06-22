function login(dialog, success, failure) {
  $(dialog)
    .load('/bookhub/login.html')
    .dialog({
      width: 400,
      height: 200,
      buttons: {
        "登录": function() {},
        "清除": function() {}
      },
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return false;
      }
    });

  $(dialog).dialog("open");
}
