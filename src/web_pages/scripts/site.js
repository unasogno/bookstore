function login(dialog, success, failure) {
  $(dialog)
    .load('/bookhub/login.html')
    .dialog({
      height: 200,
      buttons: {
        "登录": function() {
          alert($("#submit").html());
        },
        "清除": function() {
          alert($(dialog).html());
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
