function $(query) {
  return document.querySelector(query);
}

function $$(query) {
  return Array.from(document.querySelectorAll(query));
}

function hide(element) {
  element.style.setProperty('display', 'none');
}

function show(element) {
  element.style.removeProperty('display');
}

/** Hide years with no visible posts. */
function hideEmptyYears() {
  $$('.year').forEach(year => {
    const postsBlock = year.nextElementSibling;
    const posts = Array.from(postsBlock.children);
    if (posts.some(
            post => year.dataset.filtered !== 'true' &&
                post.style.getPropertyValue('display') !== 'none')) {
      show(year);
      show(postsBlock);
    } else {
      year.dataset.hposts = true;
      hide(year);
      hide(postsBlock);
    }
  });
}

function filterYears(event) {
  const act = (yearTitle, action) => {
    const yearPosts = yearTitle.nextElementSibling;
    action(yearTitle);
    action(yearPosts);
  };
  const allYears = $$('.year');
  allYears.forEach(yearTitle => {
    act(yearTitle, show);
    yearTitle.dataset.filtered = false;
  });

  const targetYear = event.target.value;
  if (targetYear !== 'all') {
    allYears.filter(yearTitle => yearTitle.id !== targetYear)
        .forEach(yearTitle => {
          act(yearTitle, hide);
          yearTitle.dataset.filtered = true;
        });
  }

  hideEmptyYears();
}

function filterDomain(event) {
  const checkbox = event.target;
  $$(`[data-domain="${checkbox.value}"]`)
      .forEach(post => checkbox.checked ? show(post) : hide(post));

  hideEmptyYears();
}

function main() {
  const yearFilter = $('[name="year-filter"]');
  yearFilter.addEventListener('change', filterYears);
  const domainFilters = $$('input[name*="-filter"]');
  domainFilters.forEach(
      filter => filter.addEventListener('change', filterDomain));
}

document.addEventListener('DOMContentLoaded', main, false);
