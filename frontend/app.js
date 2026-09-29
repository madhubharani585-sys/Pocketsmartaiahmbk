const $ = (s, r = document) => r.querySelector(s);
const inr = n => "₹" + Number(n || 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// ---- Tabs ----
document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(b => b.classList.toggle("active", b === btn));
  document.querySelectorAll(".panel").forEach(p => p.classList.toggle("active", p.id === btn.dataset.tab));
  $("#results").innerHTML = ""; $("#status").textContent = "";
}));

// ---- Home planner rows ----
const ROOMS = ["Living Room", "Kitchen", "Bedroom", "Dining Room", "Bathroom", "Balcony"];
const ITEMS = ["Lights", "Ceiling fans", "Dining table", "Sofa", "Bed", "Wardrobe", "Curtains", "Rug", "Storage shelves"];
const opts = list => list.map(o => `<option>${o}</option>`).join("");

function addRow(room = "Living Room", item = "Lights", qty = 2) {
  const div = document.createElement("div");
  div.className = "row";
  div.innerHTML = `
    <select aria-label="Room">${opts(ROOMS)}</select>
    <select aria-label="Item">${opts(ITEMS)}</select>
    <input type="number" min="1" value="${qty}" aria-label="Quantity">
    <button type="button" aria-label="Remove item">✕</button>`;
  div.children[0].value = room; div.children[1].value = item;
  div.querySelector("button").onclick = () => div.remove();
  $("#home-rows").appendChild(div);
}
$("#add-row").onclick = () => addRow();
addRow("Living Room", "Lights", 3); addRow("Living Room", "Ceiling fans", 2); addRow("Dining Room", "Dining table", 1);

// ---- Image preview ----
$("#form-jewelry [name=outfit]").addEventListener("change", e => {
  const f = e.target.files[0], img = $("#preview");
  img.hidden = !f;
  if (f) img.src = URL.createObjectURL(f);
});

// ---- Submit handling ----
async function submit(form, url, makeBody, isForm = false) {
  const btn = $("button[type=submit]", form);
  btn.disabled = true;
  $("#results").innerHTML = "";
  $("#status").className = "";
  $("#status").textContent = "Planning your budget… this takes a few seconds.";
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: isForm ? {} : { "Content-Type": "application/json" },
      body: makeBody()
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    $("#status").textContent = "";
    render(data);
  } catch (err) {
    $("#status").className = "error";
    $("#status").textContent = err.message;
  } finally {
    btn.disabled = false;
  }
}

$("#form-home").addEventListener("submit", e => {
  e.preventDefault();
  submit(e.target, "/api/home", () => JSON.stringify({
    budget: e.target.budget.value,
    items: [...document.querySelectorAll("#home-rows .row")].map(r => ({
      room: r.children[0].value, item: r.children[1].value, qty: r.children[2].value
    }))
  }));
});

$("#form-party").addEventListener("submit", e => {
  e.preventDefault();
  submit(e.target, "/api/party", () => JSON.stringify(Object.fromEntries(new FormData(e.target))));
});

$("#form-jewelry").addEventListener("submit", e => {
  e.preventDefault();
  submit(e.target, "/api/jewelry", () => new FormData(e.target), true);
});

// ---- Render results ----
function render(d) {
  const over = d.total_estimated > d.budget;
  const alloc = d.allocation.map(a => `
    <div class="bar"><strong>${esc(a.category)}</strong> — ${inr(a.amount)}
      <div class="track"><div class="fill" style="width:${Math.min(100, (a.amount / d.budget) * 100)}%"></div></div>
      <small>${esc(a.note)}</small></div>`).join("");
  const items = d.items.map(i => `
    <article class="item">
      <h3>${esc(i.name)} — ${inr(i.est_price)}</h3>
      <div class="meta">${esc(i.category)} on ${esc(i.platform)}</div>
      <p>${esc(i.why)}</p>
      <a href="${esc(i.url)}" target="_blank" rel="noopener">Search on ${esc(i.platform)}</a>
    </article>`).join("");
  const tips = d.tips.map(t => `<li>${esc(t)}</li>`).join("");
  $("#results").innerHTML = `
    <div class="summary"><p>${esc(d.summary)}</p>
      <div class="totals"><span>Budget ${inr(d.budget)}</span>
      <span class="${over ? "over" : ""}">Estimated ${inr(d.total_estimated)}</span></div></div>
    <h2>Where your money goes</h2>${alloc}
    <h2>Recommendations</h2>${items}
    ${tips ? `<h2>Tips</h2><ul>${tips}</ul>` : ""}`;
  $("#results").scrollIntoView({ behavior: "smooth" });
}
