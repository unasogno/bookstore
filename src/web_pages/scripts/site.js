function login(dialog, success, failure) {
  $(dialog)
    .load('/bookhub/login.html')
    .dialog({
      height: 200,
      buttons: {
        $("#submit_credential").html(): function() {
        },
        $("#reset_credential").html(): function() {
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
