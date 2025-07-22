// JavaScript function to toggle the menu visibility
function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// Optional: Close menu when clicking on any link inside the menu
const menuLinks = document.querySelectorAll('.menu a');
menuLinks.forEach(link => {
    link.addEventListener('click', function() {
        document.getElementById("menu").style.display = 'none';
    });
});
