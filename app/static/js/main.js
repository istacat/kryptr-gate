'use strict'

const menuBtn = document.querySelector('.menu-btn');
const menu = document.querySelector('.menu');
const overlay = document.querySelector('.overlay');


menuBtn && menuBtn.addEventListener('click', function() {
  menuBtn.classList.toggle('menu-btn--active');
  menu.classList.toggle('menu--active');
  overlay.classList.toggle('overlay--active');
});

overlay && overlay.addEventListener('click', function() {
  menuBtn.classList.toggle('menu-btn--active');
  menu.classList.toggle('menu--active');
  overlay.classList.toggle('overlay--active');
})
