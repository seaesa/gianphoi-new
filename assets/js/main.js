function initHeader() {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  if (!header || !toggle) return;

  toggle.addEventListener("click", () => {
    header.classList.toggle("nav-open");
  });

  const page = document.body.dataset.page;
  if (page) {
    header.querySelectorAll(".nav-list a").forEach((a) => {
      if (a.dataset.nav === page) a.classList.add("active");
    });
  }
}

function initFaq() {
  document.querySelectorAll(".faq-item").forEach((item) => {
    const question = item.querySelector(".faq-question");
    question.addEventListener("click", () => {
      const answer = item.querySelector(".faq-answer");
      const isOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach((openItem) => {
        if (openItem !== item) {
          openItem.classList.remove("open");
          openItem.querySelector(".faq-answer").style.maxHeight = null;
        }
      });
      item.classList.toggle("open", !isOpen);
      answer.style.maxHeight = !isOpen ? answer.scrollHeight + "px" : null;
    });
  });
}

function initContactForm() {
  const form = document.querySelector("#contact-form");
  if (!form) return;
  const success = document.querySelector("#contact-form-success");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    success.classList.add("show");
    form.reset();
    success.scrollIntoView({ behavior: "smooth", block: "center" });
  });
}

document.addEventListener("includes:loaded", initHeader);
document.addEventListener("DOMContentLoaded", () => {
  initFaq();
  initContactForm();
});
