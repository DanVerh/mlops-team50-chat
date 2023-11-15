$(document).ready(function () {
  $("#user-form").on("submit", function (e) {
    e.preventDefault();
    var current_user = $("#user_input").val();
    if (current_user) {
      var data = { username: current_user };
      $.ajax({
        url: "/api/register",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
          window.location.href = "/chat";
        },
        error: function (response) {
          console.error("Error:", response);
        }
      });
    }
  });
});
