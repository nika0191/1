(function () {
  const modal = document.getElementById("buyModal");
  const openBtn = document.getElementById("openBuyModal");
  const closeBtn = document.getElementById("closeBuyModal");
  const form = document.getElementById("buyForm");
  const success = document.getElementById("modalSuccess");

  function openModal() {
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeModal() {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  openBtn.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeModal();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    form.hidden = true;
    success.hidden = false;
  });
})();
