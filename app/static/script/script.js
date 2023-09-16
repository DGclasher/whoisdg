const popup_element = document.getElementById("popupMessage");
if(popup_element){
  setTimeout(() => {
    popup_element.style.display = "none";
  }, 5000);
}
