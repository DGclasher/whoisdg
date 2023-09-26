const popup_element = document.getElementById("popupMessage");
if (popup_element) {
  setTimeout(() => {
    popup_element.style.display = "none";
  }, 5000);
}
document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menuToggle");
  const sideMenu = document.getElementById("sideMenu");
  const menuIcon = document.querySelector("#menuToggle i");

  menuToggle.addEventListener("click", function () {
    sideMenu.classList.toggle("hidden");
    menuIcon.classList.toggle("fa-bars");
    menuIcon.classList.toggle("fa-times");
  });
});

