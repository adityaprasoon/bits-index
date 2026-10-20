const search = document.getElementById("search");
const empty = document.getElementById("empty");
const sections = document.querySelectorAll(".section");

search.addEventListener("input", () => {
  const query = search.value.trim().toLowerCase();
  let anyVisible = false;

  sections.forEach((section) => {
    const sectionMatches = section.dataset.section.toLowerCase().includes(query);
    let visibleLinks = 0;

    section.querySelectorAll("li").forEach((item) => {
      const show = sectionMatches || item.textContent.toLowerCase().includes(query);
      item.hidden = !show;
      if (show) visibleLinks++;
    });

    section.hidden = visibleLinks === 0;
    if (visibleLinks) anyVisible = true;
  });

  empty.hidden = anyVisible;
});
