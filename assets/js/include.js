async function loadIncludes() {
  const nodes = document.querySelectorAll("[data-include]");
  await Promise.all(
    [...nodes].map(async (node) => {
      const res = await fetch(node.getAttribute("data-include"));
      node.innerHTML = await res.text();
    })
  );
  document.dispatchEvent(new CustomEvent("includes:loaded"));
}

document.addEventListener("DOMContentLoaded", loadIncludes);
