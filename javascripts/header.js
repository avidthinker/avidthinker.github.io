function handler() {
  if (window.scrollY < 600) {
    document.body.classList.add("scrolled-top");
  } else {
    document.body.classList.remove("scrolled-top");
  }
}

handler();
document.addEventListener("scroll", handler);
