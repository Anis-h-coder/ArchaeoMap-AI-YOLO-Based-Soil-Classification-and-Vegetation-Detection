// === PARTICLE BACKGROUND ===
document.addEventListener("DOMContentLoaded", () => {
  const bg = document.createElement("div");
  bg.id = "particle-bg";
  document.body.appendChild(bg);

  const numParticles = 60;
  for (let i = 0; i < numParticles; i++) {
    const p = document.createElement("div");
    p.classList.add("particle");
    p.style.left = Math.random() * 100 + "%";
    p.style.bottom = Math.random() * 100 + "px";
    p.style.animationDuration = 8 + Math.random() * 8 + "s";
    p.style.animationDelay = Math.random() * 10 + "s";
    bg.appendChild(p);
  }
});

// === SMOOTH SCROLL ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth"
    });
  });
});

// === BUTTON GLOW EFFECT ===
const buttons = document.querySelectorAll('.btn');
buttons.forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    btn.style.setProperty('--x', `${x}px`);
    btn.style.setProperty('--y', `${y}px`);
  });
});
