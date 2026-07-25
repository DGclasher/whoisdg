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

  if (projectsGrid) {
    // Only fetch client-side if a data-src is configured and the loading element exists.
    const src = projectsGrid.dataset.src || "/static/data/projects.json";
    if (src && projectsLoading) {
      fetch(src)
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

  // ---------------------------
  // Experience loader
  // ---------------------------
  // Renders an array of experience objects into #experienceContainer.
  function renderExperiences(container, experiences) {
    if (!Array.isArray(experiences) || experiences.length === 0) {
      container.innerHTML =
        '<p class="text-slate-400">No experience found.</p>';
      return;
    }

    // Build HTML for each experience entry
    const html = experiences
      .map((exp) => {
        const start = exp.start_date || "";
        const end = exp.end_date || "Present";
        const dates = start ? `${start} \u2013 ${end}` : end;

        const bullets = (exp.highlights || [])
          .map((b) => `<li class="mt-1 text-slate-300">${b}</li>`)
          .join("");

        return `
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
            <div class="md:max-w-xl">
              <p class="text-sm uppercase tracking-[0.18em] text-slate-400">Experience</p>
              <h3 class="mt-2 text-2xl font-semibold text-white">${exp.company}</h3>
              <p class="text-sm text-slate-400">${exp.role} — ${exp.location || ""}</p>
              <p class="mt-1 text-sm text-slate-500">${dates}</p>
            </div>

            <div class="md:w-1/2">
              <ul class="mt-3 list-disc list-inside space-y-2 text-slate-300">
                ${bullets}
              </ul>
            </div>
          </div>
        `;
      })
      .join('<hr class="my-6 border-white/5" />');

    container.innerHTML = html;
  }

  // Load JSON from provided URL and render into the container.
  function loadExperiences(url, container) {
    const loadingEl = document.getElementById("experienceLoading");
    if (loadingEl) loadingEl.textContent = "Loading experience…";

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data) => {
        renderExperiences(container, data);
      })
      .catch((err) => {
        console.error("Failed to load experience data:", err);
        if (loadingEl) loadingEl.textContent = "Unable to load experience.";
      });
  }

  const experienceContainer = document.getElementById("experienceContainer");
  if (experienceContainer) {
    // Only perform client-side fetch if an explicit data-src is provided.
    const src = experienceContainer.dataset.src;
    if (src) {
      loadExperiences(src, experienceContainer);
    }
  }
});
