var search_result;

function submitSearch(query) {
  query = encodeURI(query);
  if (0 != query.length) {
    var ajax_url = "/api/search?query=".concat(query);
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
  alert(errorThrown);
  search_result = null;
}

function onComplete(jqXHR, status) {
  if (null == search_result) return;
  if (undefined == search_result) return;
  if ('' == search_result) return;

  loadBooks(search_result);
}

function loadBooks(idString) {
  var ids = jQuery.parseJSON(idString);
  if (0 == ids.length) return;

  $.ajax({
    url: "/books",
    type: "POST",
    data: { idList: ids.join() },
    success: function(data, status, jqXHR) {
      renderBooks(data);
    },
    error: function(jqXHR, status, errorThrown) {
      alert(status);
    },
    complete: function(jqXHR, status) {
      alert(status);
    }
  });
/*
  var id = idList[0];
  var service_url = "/book/".concat(id);
  $.ajax({
    url: service_url,
    success: function(data, status, jqXHR) {
      renderBooks(data);
    },
    error: onError,
  });
*/
}

function renderBooks(books) {
  var lines = new Array();
  lines.push("<table>");

  var headers = getHeaders(books);
  if (null == headers || undefined == headers) return;
  renderTableHeaders(headers, lines);

  for (var i = 0; i < books.length; i++) {
    renderRow(books[i], headers, lines);
  }
  lines.push("</table>");
  $("#result").html(lines.join(""));
}

function getHeaders(books) {
  var book = books[0];
  var headers = new Array();
  for(var name in book) {
    headers.push(name);
  }
  return headers;
}

function renderTableHeaders(headers, buffer) {
  buffer.push("<tr>");
  for(var i = 0; i < headers.length; i++) {
    buffer.push("<th>");
    buffer.push(headers[i]);
    buffer.push("</th>");
  }
  buffer.push("</tr>");
}

function renderRow(book, headers, buffer) {
  buffer.push("<tr>");
  for (var i = 0; i < headers.length; i++) {
    buffer.push("<td>");
    buffer.push(book[headers[i]]);
    buffer.push("</td>");
  }
  buffer.push("</tr>");
}

function loginSuccess(token) {
  $("#username").html(token);
}

function loginFailed() {
  alert('failed');
}

$(document).ready(function(){
  $("#submit").click(function(){
    var query = $("input#search-box").val();
    submitSearch(query);
  });

  var token = $.cookies.get("token");
  if (token == null) {
    begin_login("#dialog", loginSuccess, loginFailed);
  }

});
