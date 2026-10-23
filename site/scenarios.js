"use strict";
(() => {
  const select = document.getElementById("scenario-task");
  const status = document.getElementById("scenario-status");
  const input = document.getElementById("scenario-input");
  const answer = document.getElementById("scenario-answer");
  let rows = [];
  function render() {
    const row = rows.find((item) => item.task === select.value);
    if (!row) return;
    input.textContent = row.messages[1].content;
    answer.textContent = JSON.stringify(JSON.parse(row.messages[2].content), null, 2);
    status.textContent = `${row.source} · ${row.license_id} · ${row.split} · Human review pending`;
  }
  select.addEventListener("change", render);
  fetch("defensive-preview.json").then((response) => {
    if (!response.ok) throw new Error("Preview unavailable");
    return response.json();
  }).then((data) => {
    if (!Array.isArray(data) || !data.length || data.some((row) => !row.task || row.messages?.length !== 3)) {
      throw new Error("Invalid preview");
    }
    for (const row of data) JSON.parse(row.messages[2].content);
    rows = data;
    select.replaceChildren();
    for (const row of rows) {
      const option = document.createElement("option");
      option.value = row.task;
      option.textContent = row.task.replaceAll("_", " ");
      select.append(option);
    }
    select.value = rows[0].task;
    select.disabled = false;
    render();
  }).catch(() => {
    status.textContent = "The scenario preview could not load. Open the full Hugging Face dataset above.";
    input.textContent = "Preview unavailable.";
    answer.textContent = "";
    select.disabled = true;
  });
})();
