var search_result;

function submitSearch(query) {
  query = encodeURI(query);
  if (0 != query.length) {
    var ajax_url = "/search?query=".concat(query);
    console.log(ajax_url);
    $.ajax({
      url: ajax_url,
      success: onSuccess,
      error: onError,
      complete: onComplete
    });
  } else {
    alert('no input');
  }
}

function onSuccess(data, status, jqXHR) {
  search_result = data;
}

function onError(jqXHR, status, errorThrown) {
  alert(status);
  search_result = null;
}

function onComplete(jqXHR, status) {
  if (null == search_result) return;
  if (undefined == search_result) return;
  if ('' == search_result) return;

  loadBooks(search_result);
}

function loadBooks(idString) {
  var idList = jQuery.parseJSON(idString);
  if (0 == idList.length) return [];
  var id = idList[0];
  var service_url = "/book/".concat(id);
  $.ajax({
    url: service_url,
    success: function(data, status, jqXHR) {
      listBooks(data);
    },
    error: onError,
  });
}

function listBooks(books) {
  var lines = new Array();
  lines.push("<table>");
  for (var i = 0; i < books.length; i++) {
    lines.push("<tr>");
    lines.push("<td>");
    lines.push(books[i].title);
    lines.push("</td>");
    lines.push("</tr>");
  }
  lines.push("</table>");
  $("#result").html(lines.join(""));
}

$(document).ready(function(){
  $("#submit").click(function(){
    var query = $("input#query").val();
    submitSearch(query);
  });
});
