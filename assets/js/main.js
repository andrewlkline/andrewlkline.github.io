(function () {
  var STORAGE_KEY = "site-lang";
  var body = document.body;
  var toggle = document.getElementById("lang-toggle");

  function applyLang(lang) {
    body.setAttribute("data-lang", lang);
    if (toggle) {
      toggle.setAttribute("data-current", lang);
      toggle.setAttribute(
        "aria-label",
        lang === "en" ? "Switch to Tetun" : "Switch to English"
      );
    }
  }

  var saved = localStorage.getItem(STORAGE_KEY) || "en";
  applyLang(saved);

  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = body.getAttribute("data-lang") === "en" ? "tet" : "en";
      applyLang(current);
      localStorage.setItem(STORAGE_KEY, current);
    });
  }
})();
