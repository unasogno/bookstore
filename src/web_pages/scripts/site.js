function login(dialog, success, failure) {
  $(dialog).load("/bookhub/login.html");
  var submit = $("#submit_credential").html();
  var reset = $("#reset_credential").html();
  $(dialog).dialog({
      height: 200,
      buttons: {
        submit : function() {},
        reset: function() {}
      },
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return false;
      }
    });

  $(dialog).dialog("open");
}
