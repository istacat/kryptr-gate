document.addEventListener("DOMContentLoaded", function () {
  const editForm = document.querySelector(".edit__form");
  document.querySelectorAll(".field_0").forEach(function(e) {
    e.addEventListener("change", function () {
      document.getElementById("submit_0").click();
    });
  });
  document.querySelectorAll(".field_1").forEach(function(e) {
    e.addEventListener("change", function () {
      document.getElementById("submit_1").click();
    });
  });
  document.querySelectorAll(".field_2").forEach(function(e) {
    e.addEventListener("change", function () {
      document.getElementById("submit_2").click();
    });
  });
  document.querySelectorAll(".field_3").forEach(function(e) {
    e.addEventListener("change", function () {
      document.getElementById("submit_3").click();
    });
  });
  document.querySelectorAll(".field_4").forEach(function(e) {
    e.addEventListener("change", function () {
      document.getElementById("submit_4").click();
    });
  });

  if (editForm) {
    const gif = document.querySelector("#gif");
    if (gif) {
      editForm.addEventListener("submit", function () {
        gif.style.visibility = "visible";
        gif.style.height = "100%";
        document.querySelectorAll(".btn-container").forEach(function (btn) {
          btn.remove();
        });
      });
    }
  }
});
