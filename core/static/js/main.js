document.addEventListener("DOMContentLoaded", () => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* ---------- Mobile nav ---------- */
  const toggle = $(".nav__toggle"), links = $("#navLinks");
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open);
  });
  $$("#navLinks a").forEach(a => a.addEventListener("click", () => links.classList.remove("is-open")));

  /* ---------- Reveal on scroll + counters ---------- */
  const animateCount = el => {
    const target = +el.dataset.count, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "";
    const start = performance.now(), dur = 1400;
    const tick = now => {
      const p = Math.min((now - start) / dur, 1);
      el.textContent = pre + Math.round(target * (1 - Math.pow(1 - p, 3))) + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-visible");
      $$("[data-count]", e.target).forEach(animateCount);
      io.unobserve(e.target);
    });
  }, { threshold: 0.15 });
  $$(".reveal").forEach(el => io.observe(el));

  /* ---------- Preselect collateral type from a card ---------- */
  $$("[data-select-collateral]").forEach(a => a.addEventListener("click", () => {
    const sel = $("#id_collateral_type");
    if (sel) sel.value = a.dataset.selectCollateral;
  }));

  /* ---------- Repayment estimator ---------- */
  const calcBox = $("#calculator");
  const cur = calcBox.dataset.currency || "$";
  const amt = $("#calcAmount"), rate = $("#calcRate"), term = $("#calcTerm");
  const fmt = n => cur + Math.round(n).toLocaleString("en-US");
  const calc = () => {
    const P = +amt.value, r = +rate.value / 100, n = +term.value;
    const pay = r === 0 ? P / n : (P * r) / (1 - Math.pow(1 + r, -n));
    $("#amtOut").textContent = fmt(P);
    $("#rateOut").textContent = (+rate.value).toFixed(1) + "%";
    $("#termOut").textContent = term.value + (+term.value === 1 ? " month" : " months");
    $("#calcPayment").textContent = fmt(pay);
    $("#calcInterest").textContent = fmt(pay * n - P);
  };
  [amt, rate, term].forEach(i => i.addEventListener("input", calc));
  calc();

  /* Prefill the request amount from the estimator */
  const amountField = $("#id_loan_amount");
  $$("[data-select-collateral], .calc__result .btn").forEach(a =>
    a.addEventListener("click", () => { if (amountField && !amountField.value) amountField.value = amt.value; })
  );

  /* ---------- Process timeline ---------- */
  const steps = $$(".step"), panels = $$(".panel"), fill = $("#timelineFill");
  const setStep = n => {
    steps.forEach((s, i) => {
      s.classList.toggle("is-active", i + 1 === n);
      s.classList.toggle("is-done", i + 1 < n);
    });
    panels.forEach(p => p.classList.toggle("is-active", +p.dataset.panel === n));
    fill.style.width = ((n - 1) / (steps.length - 1)) * 100 + "%";
  };
  steps.forEach(s => s.addEventListener("click", () => setStep(+s.dataset.step)));
  setStep(1);

  /* ---------- Testimonial slider ---------- */
  const track = $("#sliderTrack"), slides = $$(".quote", track), dots = $("#sliderDots");
  let idx = 0, timer;
  slides.forEach((_, i) => {
    const b = document.createElement("button");
    b.setAttribute("aria-label", "Go to testimonial " + (i + 1));
    b.addEventListener("click", () => go(i, true));
    dots.appendChild(b);
  });
  function go(i, manual) {
    idx = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${idx * 100}%)`;
    $$("button", dots).forEach((d, k) => d.classList.toggle("is-active", k === idx));
    if (manual) restart();
  }
  const restart = () => { clearInterval(timer); timer = setInterval(() => go(idx + 1), 6000); };
  $$(".slider__btn").forEach(b => b.addEventListener("click", () => go(idx + +b.dataset.dir, true)));
  go(0); restart();

  /* ---------- Collateral photo previews ---------- */
  const MAX_FILES = 5, MAX_MB = 5;
  const fileInput = $("#id_images"), previews = $("#imagePreviews");
  const imgError = $('[data-error-for="images"]');
  const clearPreviews = () => {
    $$("img", previews).forEach(i => URL.revokeObjectURL(i.src));
    previews.innerHTML = "";
  };
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      clearPreviews(); imgError.textContent = "";
      const files = Array.from(fileInput.files);
      if (files.length > MAX_FILES) {
        imgError.textContent = `You can upload up to ${MAX_FILES} photos.`;
        fileInput.value = ""; return;
      }
      const tooBig = files.find(f => f.size > MAX_MB * 1024 * 1024);
      if (tooBig) {
        imgError.textContent = `'${tooBig.name}' is larger than ${MAX_MB}MB.`;
        fileInput.value = ""; return;
      }
      files.forEach(f => {
        if (!f.type.startsWith("image/")) return;
        const img = document.createElement("img");
        img.src = URL.createObjectURL(f); img.alt = f.name;
        previews.appendChild(img);
      });
    });
  }

  /* ---------- Loan request form (AJAX with graceful fallback) ---------- */
  const form = $("#leadForm"), btn = $("#submitBtn"), ok = $("#formSuccess");
  const clearErrors = () => $$(".field__error").forEach(e => (e.textContent = ""));
  form.addEventListener("submit", async e => {
    e.preventDefault();
    clearErrors(); ok.hidden = true;
    btn.disabled = true; btn.textContent = "Sending...";
    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      const data = await res.json();
      if (data.ok) {
        ok.textContent = data.message; ok.hidden = false;
        form.reset(); clearPreviews();
        ok.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        Object.entries(data.errors || {}).forEach(([name, errs]) => {
          const el = $(`[data-error-for="${name}"]`);
          if (el) el.textContent = errs.map(x => x.message).join(" ");
        });
      }
    } catch (err) {
      form.submit(); // fall back to a normal POST
      return;
    } finally {
      btn.disabled = false; btn.textContent = "Submit Loan Request";
    }
  });
});
