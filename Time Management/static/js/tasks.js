document.addEventListener("DOMContentLoaded", function() {
  const accordions = document.querySelectorAll(".task-accordion");

  accordions.forEach(accordion => {
      const tag = accordion.querySelector(".tag");
      const panel = accordion.querySelector(".task-panel");
      tag.addEventListener("click", () => {
          // Check if the clicked tag's panel is currently open
          const isOpen = accordion.classList.contains("active");

          // Toggle the "active" class on the clicked accordion
          accordion.classList.toggle("active", !isOpen);
      });
  });
});

