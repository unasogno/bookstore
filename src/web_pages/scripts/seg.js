var search_result;

function submitSearch(query) {
  var query = $("input#query").val();
  query = encodeURI(query);
  if (0 != query.length) {
    var ajax_url = "/search?query=".concat(query);
    console.log(ajax_url);
    $.ajax({
      url: "/search?query=".concat(query),
      success: onSuccess,
      error: onError,
      complete: onComplete
    });
  } else {
    alert('请输入搜索内容');
  }
}

function onSuccess(data, status, jqXHR) {
  alert(status);
  search_result = data;
}

function onError(jqXHR, status, errorThrown) {
  alert(status);
  search_result = null;
}

function onComplete(jqXHR, status) {
  if (null == search_result) return;
  if (undefined == search_result) return;
  idList = jQuery.parseJSON(search_result);
  if (0 == idList.length) return;
  alert(idList[0]);
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
