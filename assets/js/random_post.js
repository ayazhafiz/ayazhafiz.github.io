function $(query) {
  return document.querySelector(query);
}

function gotoRandomPost(event) {
  const randomPost =
      gwwPostUrls[Math.floor(Math.random() * gwwPostUrls.length)];
  location.href = randomPost;
}

function main() {
  const rpButton = $('#random-post');
  rpButton.addEventListener('click', gotoRandomPost)
}

document.addEventListener('DOMContentLoaded', main, false);
