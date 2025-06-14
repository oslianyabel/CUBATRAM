// static/js/hero.js
document.addEventListener('DOMContentLoaded', function() {
    // Cierra los menús al hacer click fuera
    document.addEventListener('click', function(event) {
        if (!event.target.matches('.dropdown-toggle')) {
            var dropdowns = document.getElementsByClassName("dropdown-menu");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.style.display === 'block') {
                    openDropdown.style.display = 'none';
                }
            }
        }
    });
    
    // Alternar menús al hacer click
    var dropdownToggles = document.getElementsByClassName("dropdown-toggle");
    for (var i = 0; i < dropdownToggles.length; i++) {
        dropdownToggles[i].addEventListener('click', function() {
            var menu = this.nextElementSibling;
            if (menu.style.display === 'block') {
                menu.style.display = 'none';
            } else {
                menu.style.display = 'block';
            }
        });
    }
});