const popup_element = document.getElementById("popupMessage");
if(popup_element){
  setTimeout(() => {
    popup_element.style.display = "none";
  }, 5000);
}
function openSideMenu() {
  document.getElementById("sideMenu").style.width = "250px"; // Adjust the width as needed
}

function closeSideMenu() {
  document.getElementById("sideMenu").style.width = "0";
}

// Toggle the side menu when the toggle button is clicked
document.getElementById("menuToggle").addEventListener("click", function() {
  openSideMenu();
});

// Close the side menu when the close button is clicked
document.getElementById("menuClose").addEventListener("click", function() {
  closeSideMenu();
});