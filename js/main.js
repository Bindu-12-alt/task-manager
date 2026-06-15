// ========== NAVBAR SCROLL ==========
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ========== MOBILE MENU ==========
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');
const mobileClose = document.getElementById('mobileClose');

hamburger?.addEventListener('click', () => mobileNav.classList.add('active'));
mobileClose?.addEventListener('click', () => mobileNav.classList.remove('active'));

mobileNav?.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => mobileNav.classList.remove('active'));
});

// ========== SCROLL ANIMATIONS ==========
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// ========== CONTACT FORM ==========
const form = document.getElementById('contactForm');
const successMsg = document.getElementById('successMsg');

form?.addEventListener('submit', (e) => {
  e.preventDefault();

  const required = form.querySelectorAll('[required]');
  let valid = true;

  required.forEach(field => {
    field.style.borderColor = '';
    if (!field.value.trim()) {
      field.style.borderColor = '#ef4444';
      valid = false;
    }
  });

  if (!valid) return;

  const btn = form.querySelector('.form-submit');
  btn.textContent = 'Sending...';
  btn.disabled = true;

  setTimeout(() => {
    form.reset();
    btn.textContent = 'Send Message ➜';
    btn.disabled = false;
    successMsg.style.display = 'block';
    setTimeout(() => successMsg.style.display = 'none', 6000);
  }, 1500);
});

// ========== ACTIVE NAV LINK ==========
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(link => {
  const href = link.getAttribute('href');
  if (href === currentPage || (currentPage === '' && href === 'index.html')) {
    link.style.color = '#60a5fa';
  }
});
