// Search and filters for /bibliography/. The page is fully readable without
// this script; it only hides entries, sections and TOC links that don't match.
(function () {
  var search = document.getElementById("bib-search");
  if (!search) return;

  var selects = Array.prototype.slice.call(document.querySelectorAll(".bib-controls select[data-facet]"));
  var entries = Array.prototype.slice.call(document.querySelectorAll(".bib-entry"));
  var sections = Array.prototype.slice.call(document.querySelectorAll(".bib-section"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".bib-group"));
  var tocItems = Array.prototype.slice.call(document.querySelectorAll(".bib-jump a[data-target]"));
  var count = document.getElementById("bib-count");
  var empty = document.getElementById("bib-empty");
  var total = uniqueKeys(entries);

  function uniqueKeys(list) {
    var seen = {};
    list.forEach(function (e) { seen[e.getAttribute("data-key")] = true; });
    return Object.keys(seen).length;
  }

  function matches(entry, terms, filters) {
    for (var facet in filters) {
      var attr = facet === "family" ? entry.getAttribute("data-family").split(" ")
                                    : (entry.getAttribute("data-" + facet) || "").split("|");
      if (attr.indexOf(filters[facet]) === -1) return false;
    }
    var hay = entry.getAttribute("data-search");
    for (var i = 0; i < terms.length; i++) {
      if (hay.indexOf(terms[i]) === -1) return false;
    }
    return true;
  }

  function apply() {
    var terms = search.value.toLowerCase().split(/\s+/).filter(Boolean);
    var filters = {};
    selects.forEach(function (s) { if (s.value) filters[s.getAttribute("data-facet")] = s.value; });
    var active = terms.length || Object.keys(filters).length;

    var visible = [];
    entries.forEach(function (e) {
      var ok = !active || matches(e, terms, filters);
      e.hidden = !ok;
      if (ok) visible.push(e);
    });

    var shownSections = {};
    sections.forEach(function (s) {
      var any = s.querySelector(".bib-entry:not([hidden])");
      s.hidden = !any;
      if (any) shownSections[s.id] = true;
    });
    groups.forEach(function (g) { g.hidden = !g.querySelector(".bib-section:not([hidden])"); });
    tocItems.forEach(function (li) { li.hidden = !shownSections[li.getAttribute("data-target")]; });
    document.querySelectorAll(".bib-jump-row").forEach(function (row) {
      row.hidden = !row.querySelector("a[data-target]:not([hidden])");
    });

    var n = uniqueKeys(visible);
    if (count) {
      count.innerHTML = active
        ? '<span lang="en">Showing ' + n + " of " + total + ' entries</span><span lang="tet">Hatudu ' + n + " husi " + total + "</span>"
        : '<span lang="en">' + total + ' entries</span><span lang="tet">' + total + " entrada</span>";
    }
    if (empty) empty.hidden = n > 0;
  }

  search.addEventListener("input", apply);
  selects.forEach(function (s) { s.addEventListener("change", apply); });
  apply();
})();
