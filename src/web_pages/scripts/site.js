function login(dialog, success, failure) {
  $(dialog).dialog({
    autoOpen: false,
    modal: true,
    beforeClose: function (event, ui) {
      return false;
    }
  });

  $(dialog).dialog("open");
}
