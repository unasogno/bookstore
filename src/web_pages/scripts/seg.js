
$(document).ready(function(){
  $("#submit").click(function(){
    var query = $("input#query").val();
    if (0 != query.length) {
      $.ajax({
        url: "/search?query=".concat(query),
        success: function(data, status, jqXHR) {
          alert(data);
        },
        error: function(jqXHR, status, errorThrown) {
          alert(status);
        },
        complete: function(jqXHR, status) {
          alert('complete');
        }
    }
  });
});
