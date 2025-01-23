document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.getElementById("darkModeToggle");

    // Check localStorage and apply dark mode if enabled
    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
    }

    darkModeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            enableDarkMode();
            localStorage.setItem('darkMode', 'enabled');
        } else {
            disableDarkMode();
            localStorage.setItem('darkMode', 'disabled');
        }
    });

    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        const icon = darkModeToggle.querySelector('i');
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");

        // Toggle dark mode for items, info, and precio
        const nav = document.querySelectorAll(".nav");
        nav.forEach(nav => nav.classList.add("dark-mode"));

        const links = document.querySelectorAll(".nav-link");
        links.forEach(links => links.classList.add("dark-mode"));

        const themeIcon = document.querySelectorAll(".theme-icon");
        themeIcon.forEach(themeIcon => themeIcon.classList.add("dark-mode"));

        const search  = document.querySelectorAll(".search-input ");
        search.forEach(search => search.classList.add("dark-mode"));

        const cardHeader  = document.querySelectorAll(".card-header ");
        cardHeader.forEach(cardHeader => cardHeader.classList.add("dark-mode"));

        const cardFooter  = document.querySelectorAll(".card-footer ");
        cardFooter.forEach(cardFooter => cardFooter.classList.add("dark-mode"));

        const table  = document.querySelectorAll(".table");
        table.forEach(table => table.classList.add("dark-mode"));

        const th  = document.querySelectorAll(".th");
        th.forEach(th => th.classList.add("dark-mode"));

        const td  = document.querySelectorAll(".td");
        td.forEach(td => td.classList.add("dark-mode"));

        const reporte  = document.querySelectorAll(".card-falla");
        reporte.forEach(reporte => reporte.classList.add("dark-mode"));

        const date  = document.querySelectorAll(".date-input");
        date.forEach(date => date.classList.add("dark-mode"));

        const dateCont  = document.querySelectorAll(".date-input__container");
        dateCont.forEach(dateCont => dateCont.classList.add("dark-mode"));

        const form  = document.querySelectorAll(".form");
        form.forEach(formitem => formitem.classList.add("dark-mode"));

        const registForm  = document.querySelectorAll(".regist__form");
        registForm.forEach(form => form.classList.add("dark-mode"));

        const btnFechas  = document.querySelectorAll(".btn-fechas");
        btnFechas.forEach(btn => btn.classList.add("dark-mode"));

        const modal  = document.querySelectorAll(".modal-content");
        modal.forEach(modal => modal.classList.add("dark-mode"));

        const modalb  = document.querySelectorAll(".form-control");
        modalb.forEach(modal => modal.classList.add("dark-mode"));

        const menuButton  = document.querySelectorAll(".menu-button");
        menuButton.forEach(button => button.classList.add("dark-mode"));



    }

    function disableDarkMode() {
        document.body.classList.remove('dark-mode');
        const icon = darkModeToggle.querySelector('i');
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");

        // Toggle dark mode off for items, info, and precio
        const nav = document.querySelectorAll(".nav");
        nav.forEach(nav => nav.classList.remove("dark-mode"));

        const links = document.querySelectorAll(".nav-link");
        links.forEach(links => links.classList.remove("dark-mode"));

        const themeIcon = document.querySelectorAll(".theme-icon");
        themeIcon.forEach(themeIcon => themeIcon.classList.remove("dark-mode"));

        const containers = document.querySelectorAll(".containers");
        containers.forEach(precio => precio.classList.remove("dark-mode"));

        const cardHeader  = document.querySelectorAll(".card-header ");
        cardHeader.forEach(cardHeader => cardHeader.classList.remove("dark-mode"));

        const cardFooter  = document.querySelectorAll(".card-footer ");
        cardFooter.forEach(cardFooter => cardFooter.classList.remove("dark-mode"));

        const table  = document.querySelectorAll(".table");
        table.forEach(table => table.classList.remove("dark-mode"));

        const th  = document.querySelectorAll(".th");
        th.forEach(th => th.classList.remove("dark-mode"));

        const td  = document.querySelectorAll(".td");
        td.forEach(td => td.classList.remove("dark-mode"));

        const reporte  = document.querySelectorAll(".card-falla");
        reporte.forEach(reporte => reporte.classList.remove("dark-mode"));

        const date  = document.querySelectorAll(".date-input");
        date.forEach(date => date.classList.remove("dark-mode"));

        const dateCont  = document.querySelectorAll(".date-input__container");
        dateCont.forEach(dateCont => dateCont.classList.remove("dark-mode"));

        const form  = document.querySelectorAll(".form");
        form.forEach(formitem => formitem.classList.remove("dark-mode"));

        const registForm  = document.querySelectorAll(".regist__form");
        registForm.forEach(form => form.classList.remove("dark-mode"));

        const btnFechas  = document.querySelectorAll(".btn-fechas");
        btnFechas.forEach(btn => btn.classList.remove("dark-mode"));

        const modal  = document.querySelectorAll(".modal-content");
        modal.forEach(modal => modal.classList.remove("dark-mode"));

        const modalb  = document.querySelectorAll(".form-control");
        modalb.forEach(modal => modal.classList.remove("dark-mode"));

        const menuButton  = document.querySelectorAll(".menu-button");
        menuButton.forEach(button => button.classList.remove("dark-mode"));


    }
});