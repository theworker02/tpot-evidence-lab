"use strict";
const $ = (id) => document.getElementById(id);
let rows = [], filtered = [], page = 0;
const pageSize = 12;
function render() {
  const query = $("query").value.trim().toLowerCase();
  filtered = rows.filter((row) => (!$("corpus").value || row.corpus === $("corpus").value)
    && (!$("sensor").value || row.sensor === $("sensor").value)
    && [row.id, row.sensor, row.transport, row.destination_port].join(" ").toLowerCase().includes(query));
  const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
  page = Math.min(page, pages - 1);
  $("records").replaceChildren();
  for (const row of filtered.slice(page * pageSize, (page + 1) * pageSize)) {
    const tr = document.createElement("tr");
    for (const value of [row.id, row.timestamp_utc, row.sensor, row.transport, row.destination_port ?? "Unknown", row.label_basis]) {
      const td = document.createElement("td");
      td.textContent = String(value);
      tr.append(td);
    }
    $("records").append(tr);
  }
  $("status").textContent = filtered.length ? `${filtered.length} matching preview records · ${rows.length} preview records loaded` : "No preview records match. Clear the search or reset the filters.";
  $("page").textContent = `Page ${page + 1} of ${pages}`;
  $("previous").disabled = page === 0;
  $("next").disabled = page + 1 >= pages;
}
$("filters").addEventListener("submit", (event) => event.preventDefault());
$("filters").addEventListener("input", () => { page = 0; render(); });
$("filters").addEventListener("change", () => { page = 0; render(); });
$("filters").addEventListener("reset", () => { setTimeout(() => { page = 0; render(); }, 0); });
$("previous").addEventListener("click", () => { page -= 1; render(); });
$("next").addEventListener("click", () => { page += 1; render(); });
fetch("preview.json").then((response) => {
  if (!response.ok) throw new Error("Preview unavailable");
  return response.json();
}).then((data) => {
  if (!Array.isArray(data.rows) || !data.rows.length) throw new Error("Preview is empty");
  rows = data.rows;
  for (const sensor of [...new Set(rows.map((row) => row.sensor))].sort()) {
    const option = document.createElement("option"); option.value = sensor; option.textContent = sensor; $("sensor").append(option);
  }
  render();
}).catch(() => { $("status").textContent = "The preview could not load. Reload or open the full dataset using the Hugging Face link above."; });
