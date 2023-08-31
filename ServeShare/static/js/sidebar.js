document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector('.sidebar');
    const sidebarContainer = sidebar.querySelector('.sidebar-1');

    sidebar.addEventListener('click', function () {
        sidebarContainer.classList.toggle('expanded');
    });
});
// const sidebar = document.getElementById('sidebar');

// sidebar.addEventListener('click', () => {
//     sidebar.classList.toggle('expanded');
// });
