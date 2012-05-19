var search_result;

function submitSearch(query) {
  var query = $("input#query").val();
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

  var books = loadBooks(search_result);
  if (0 == books.length) return;

  listBooks(books);
}

function loadBooks(idString) {
  var idList = jQuery.parseJSON(idString);
  if (0 == idList.length) return [];
  var id = idList[0];
  var service_url = "/book/".concat(id);
  $.ajax({
    url: service_url,
    success: onLoadBooksSuccess,
    error: onError,
  });
}

function onLoadBooksSuccess(data, status, jqXHR) {
  var book = jQuery.parseJSON(data);
  var books = [book];

  listBooks(books);
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
