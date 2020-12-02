function $(query) {
  return document.querySelector(query);
}

function main() {
  const fly = $('.fly');
  const hue = Math.floor(Math.random() * 360);
  fly.style.filter = `hue-rotate(${hue}deg)`;
}

document.addEventListener('DOMContentLoaded', main, false);
