function login(dialog, success, failure) {
  $(dialog).dialog({
    autoOpen: false,
    modal: true,
    close: function (event, ui) {
      
    }
  });

  $(dialog).dialog("open");
}
