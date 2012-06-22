function login(dialog, success, failure) {
  $(dialog)
    .load('/bookhub/login.html')
    .dialog({
      width: 400,
      height: 200,
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return false;
      }
    });

  $(dialog).dialog("open");
}
