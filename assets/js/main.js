/* "Thép & Nắng" — script cho site tĩnh. Vanilla, không dependency.
   Mỗi module tự thoát nếu không tìm thấy phần tử của mình, vì cùng một file
   chạy trên mọi trang. */

// Cờ cho CSS biết JS đã chạy (và để kiểm tra nhanh khi debug).
document.documentElement.dataset.js = "ready";

const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
);

/* -------------------------------------------------- 1. Menu mobile */

function initNav() {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  if (!header || !toggle) return;

  const setOpen = (open) => {
    header.dataset.navOpen = open ? "true" : "false";
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Đóng menu" : "Mở menu");
  };

  setOpen(false);

  toggle.addEventListener("click", () => {
    setOpen(header.dataset.navOpen !== "true");
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (header.dataset.navOpen !== "true") return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (event) => {
    if (header.dataset.navOpen !== "true") return;
    if (header.contains(event.target)) return;
    setOpen(false);
  });
}

/* -------------------------------------------------- 1b. Dropdown dịch vụ */

function initServicesMenu() {
  const toggle = document.querySelector(".nav__toggle");
  if (!toggle) return;

  const menuId = toggle.getAttribute("aria-controls");
  const menu = menuId ? document.getElementById(menuId) : null;
  if (!menu) return;

  const setOpen = (open) => {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute(
      "aria-label",
      open ? "Đóng danh sách dịch vụ" : "Mở danh sách dịch vụ"
    );
  };

  toggle.addEventListener("click", () => {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (toggle.getAttribute("aria-expanded") !== "true") return;
    setOpen(false);
    toggle.focus();
  });

  document.addEventListener("click", (event) => {
    if (toggle.getAttribute("aria-expanded") !== "true") return;
    if (toggle.contains(event.target) || menu.contains(event.target)) return;
    setOpen(false);
  });
}

/* -------------------------------------------------- 2. FAQ accordion */

function initFaq() {
  const questions = document.querySelectorAll(".faq__question");
  if (!questions.length) return;

  questions.forEach((question) => {
    question.addEventListener("click", () => {
      const panelId = question.getAttribute("aria-controls");
      const panel = panelId ? document.getElementById(panelId) : null;
      if (!panel) return;

      const isOpen = question.getAttribute("aria-expanded") === "true";
      const list = question.closest(".faq");

      if (list) {
        list.querySelectorAll('.faq__question[aria-expanded="true"]').forEach(
          (other) => {
            if (other === question) return;
            other.setAttribute("aria-expanded", "false");
            const otherId = other.getAttribute("aria-controls");
            const otherPanel = otherId ? document.getElementById(otherId) : null;
            if (otherPanel) otherPanel.hidden = true;
          }
        );
      }

      question.setAttribute("aria-expanded", isOpen ? "false" : "true");
      panel.hidden = isOpen;
    });
  });
}

/* -------------------------------------------------- 3. Sticky action bar */

function initStickyBar() {
  const bar = document.querySelector(".sticky-bar");
  if (!bar) return;
  if (prefersReducedMotion.matches) return;

  let lastY = window.scrollY;

  window.addEventListener(
    "scroll",
    () => {
      const y = window.scrollY;
      // Cuộn xuống thì hiện, cuộn lên thì nhường chỗ cho nội dung.
      if (Math.abs(y - lastY) > 8) {
        bar.dataset.hidden = y < lastY && y > 200 ? "true" : "false";
        lastY = y;
      }
    },
    { passive: true }
  );
}

/* -------------------------------------------------- 4. Lọc bài blog */

function initChips() {
  const chips = document.querySelectorAll(".chip[data-filter]");
  const grid = document.getElementById("post-grid");
  if (!chips.length || !grid) return;

  const empty = document.getElementById("post-empty");
  const cards = grid.querySelectorAll("[data-category]");

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const filter = chip.dataset.filter;

      chips.forEach((other) => {
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });

      let visible = 0;
      cards.forEach((card) => {
        const match = filter === "all" || card.dataset.category === filter;
        card.hidden = !match;
        if (match) visible += 1;
      });

      if (empty) empty.hidden = visible > 0;
    });
  });
}

/* -------------------------------------------------- 5. Form báo giá */

const VALIDATORS = {
  name: (value) =>
    value.trim().length >= 2 ? "" : "Vui lòng nhập họ tên của bạn.",
  phone: (value) =>
    /^[0-9+\s.]{9,15}$/.test(value.trim())
      ? ""
      : "Số điện thoại chưa đúng định dạng.",
};

function initQuoteForm() {
  const form = document.getElementById("quote-form");
  if (!form) return;

  const success = document.getElementById("quote-form-success");

  // Card dịch vụ dẫn tới đây kèm ?dich-vu=<slug> — chọn sẵn đúng mục.
  const wanted = new URLSearchParams(window.location.search).get("dich-vu");
  const select = form.querySelector("#service");
  if (wanted && select) {
    const option = select.querySelector(`option[value="${CSS.escape(wanted)}"]`);
    if (option) select.value = wanted;
  }

  const showError = (field, message) => {
    const wrapper = field.closest(".field");
    const box = wrapper ? wrapper.querySelector(".field__error") : null;
    if (box) box.textContent = message;
    if (wrapper) wrapper.dataset.invalid = message ? "true" : "false";
    field.setAttribute("aria-invalid", message ? "true" : "false");
    return !message;
  };

  Object.keys(VALIDATORS).forEach((id) => {
    const field = form.querySelector(`#${id}`);
    if (!field) return;
    field.addEventListener("blur", () => {
      showError(field, VALIDATORS[id](field.value));
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    let firstInvalid = null;
    Object.keys(VALIDATORS).forEach((id) => {
      const field = form.querySelector(`#${id}`);
      if (!field) return;
      const ok = showError(field, VALIDATORS[id](field.value));
      if (!ok && !firstInvalid) firstInvalid = field;
    });

    if (firstInvalid) {
      firstInvalid.focus();
      return;
    }

    // TODO: form chưa nối endpoint thật — hiện chỉ giả lập thành công ở client.
    // Để gửi đi thật, thay khối dưới bằng một trong hai cách:
    //   1. fetch() tới endpoint Formspree / Web3Forms với new FormData(form)
    //   2. chuyển hướng sang Zalo kèm nội dung soạn sẵn từ các trường
    if (success) {
      success.hidden = false;
      success.scrollIntoView({
        behavior: prefersReducedMotion.matches ? "auto" : "smooth",
        block: "center",
      });
    }
    form.reset();
  });
}

/* -------------------------------------------------- khởi động */

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  initServicesMenu();
  initFaq();
  initStickyBar();
  initChips();
  initQuoteForm();
});
