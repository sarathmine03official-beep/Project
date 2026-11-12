document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("-translate-x-full");
  });
});
