const popup_element = document.getElementById("popupMessage");
if (popup_element) {
  setTimeout(() => {
    popup_element.style.display = "none";
  }, 5000);
}

document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menuToggle");
  const sideMenu = document.getElementById("sideMenu");
  const menuIcon = document.querySelector("#menuToggle i");

  if (menuToggle && sideMenu && menuIcon) {
    menuToggle.addEventListener("click", function () {
      if (sideMenu.classList.contains("translate-x-full")) {
        sideMenu.classList.remove("translate-x-full");
        menuIcon.classList.remove("fa-bars");
        menuIcon.classList.add("fa-times");
      } else {
        sideMenu.classList.add("translate-x-full");
        menuIcon.classList.remove("fa-times");
        menuIcon.classList.add("fa-bars");
      }
    });
  }

  const projectsGrid = document.getElementById("projectsGrid");
  const projectsLoading = document.getElementById("projectsLoading");

  if (projectsGrid && projectsLoading) {
    fetch("/static/data/projects.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((projects) => {
        if (!Array.isArray(projects) || projects.length === 0) {
          projectsLoading.textContent = "No projects found.";
          return;
        }

        projectsLoading.style.display = "none";
        projectsGrid.innerHTML = projects
          .map((project) => {
            const tags = project.tags
              .map(
                (tag) =>
                  `<span class="inline-flex rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">${tag}</span>`,
              )
              .join("");

            return `
              <article class="glass-card flex flex-col justify-between rounded-[28px] p-6 shadow-2xl shadow-black/20">
                <div>
                  <p class="text-sm uppercase tracking-[0.22em] text-lime-400">Project</p>
                  <h3 class="mt-4 text-2xl font-semibold text-white">${project.title}</h3>
                  <p class="mt-4 text-slate-400">${project.description}</p>
                </div>
                <div class="mt-6 flex flex-wrap gap-2">${tags}</div>
                <div class="mt-6 flex flex-wrap gap-3">
                  <a href="${project.demo}" target="_blank" class="rounded-full border border-lime-500/20 bg-lime-500/10 px-4 py-2 text-sm font-semibold text-lime-300 transition hover:bg-lime-500/20">Demo</a>
                  <a href="${project.repo}" target="_blank" class="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white transition hover:border-lime-500">Repo</a>
                </div>
              </article>
            `;
          })
          .join("");
      })
      .catch((error) => {
        console.error("Failed to load projects:", error);
        projectsLoading.textContent = "Unable to load projects.";
      });
  }
});
