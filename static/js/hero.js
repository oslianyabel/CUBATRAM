document.addEventListener('DOMContentLoaded', function() {
    // Cierra los menús al hacer click fuera
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.dropdown')) {
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
        dropdownToggles[i].addEventListener('click', function(e) {
            e.stopPropagation();
            var menu = this.closest('.dropdown').querySelector(".dropdown-menu");
            if (menu.style.display === 'block') {
                menu.style.display = 'none';
            } else {
                menu.style.display = 'block';
            }
        });
    }
    
    // Evitar que el menú se cierre al hacer click en los checkboxes
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});