function login(dialog, success, failure) {
  $(dialog)
    .html("user name: <input type=\"text\" id=\"username\" ></input>")
    .dialog({
      autoOpen: false,
      modal: true,
      beforeClose: function (event, ui) {
        return false;
      }
    });

  $(dialog).dialog("open");
}
