var search_result;
function onSuccess(data, status, jqXHR) {
  alert(status);
  search_result = data;
}

function onError(jqXHR, status, errorThrown) {
  alert(status);
  search_result = null;
}

function onComplete(jqXHR, status) {
  alert(status);
  alert(search_result);
}

$(document).ready(function(){
  $("#submit").click(function(){
    var query = $("input#query").val();
    query = encodeURI(query);
    if (0 != query.length) {
      var ajax_url = "/search?query=".concat(query);
      alert(ajax_url);
      $.ajax({
        url: "/search?query=".concat(query),
        success: onSuccess,
        error: onError,
        complete: onComplete
      });
    }
  });
});
