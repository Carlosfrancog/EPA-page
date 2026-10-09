const menuButton = document.querySelector('[data-menu-button]');
const nav = document.querySelector('[data-nav]');
if (menuButton && nav) {
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      menuButton.setAttribute('aria-expanded', 'false');
      nav.classList.remove('open');
    }
  });
}

const statusTarget = document.querySelector('[data-repo-status]');
if (statusTarget) {
  fetch(statusTarget.dataset.source)
    .then((response) => { if (!response.ok) throw new Error('status unavailable'); return response.json(); })
    .then((data) => {
      if (!data.commit || !data.url) return;
      const link = document.createElement('a');
      link.href = data.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = `${data.commit.slice(0, 7)} · ${data.subject}`;
      statusTarget.replaceChildren(link);
    })
    .catch(() => { statusTarget.textContent = 'Atualização do repositório indisponível'; });
}
