var menu = document.querySelector(".nav-flyout-menu");

function toggleFlyoutMenu() {
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
}