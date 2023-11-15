
$(document).ready(function () {
  var current_user;
  var socket = new WebSocket("ws://127.0.0.1:8000/api/chat");

  function getMarkFromStatus(status) {
    switch (status) {
      case "Good":
        return "<span style='color: green;'>🟢</span>";
      case "Bad":
        return "<span style='color: red;'>🔴</span>";
      case "error":
        return "<span style='color: red;'>❓</span>";
      default:
        return "<span style='color: grey;'>⏳</span>";
    }
  }
  
  $.get("/api/current_user", function (response) {
    current_user = response;
    $("#profile").text(current_user);
  });

  socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var parent = $("#messages");
    // Check if the message is an update or a new message
    if (data.sender && data.message) {
      var sender = data.sender == current_user ? "You" : data.sender;
      var message = data.message;
      var messageId = data.message_id;
      var content = `<p id="message-${messageId}"><strong>${sender}</strong>: ${message}`;
      content += ` <span id='mark-${messageId}'></span></p>`;
      parent.append(content);
    } else if (data.message_id && data.censorship_status) {
      // Update to an existing message with a censorship result
      var markElement = $(`#mark-${data.message_id}`);
      var mark = getMarkFromStatus(data.censorship_status);
      markElement.html(mark); // Update the mark placeholder with the actual mark
    }
  };

  $("#chat-form").on("submit", function (e) {
    e.preventDefault();
    var message = $("#chat-form input").val();
    if (message) {
      var data = {
        sender: current_user,
        message: message,
      };
      socket.send(JSON.stringify(data));
      $("#chat-form input").val(""); // Clear the input after sending the message
      document.cookie = "X-Authorization=; path=/;";
    }
  });
});
