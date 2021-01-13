const menuBtn = document.querySelector('.menu-btn');
const menu = document.querySelector('.menu');
const overlay = document.querySelector('.overlay');


menuBtn && menuBtn.addEventListener('click', function () {
  menuBtn.classList.toggle('menu-btn--active');
  menu.classList.toggle('menu--active');
  overlay.classList.toggle('overlay--active');
});

overlay && overlay.addEventListener('click', function () {
  menuBtn.classList.toggle('menu-btn--active');
  menu.classList.toggle('menu--active');
  overlay.classList.toggle('overlay--active');
})

if (document.getElementById('users-table')) {
  table = new Tabulator("#users-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/user_list',
    columns: [ //Define Table Columns
      { title: "Id", field: "id" },
      { title: "Username", field: "username", hozAlign: "left" },
      { title: "Email", field: "email" },
      { title: "Activated", field: "activated" },
      { title: "Role", field: "role" },
      { title: "Created", field: "created_at", sorter: "date", hozAlign: "center" },
    ],
    rowClick: function (e, row) { //trigger an alert message when the row is clicked
      alert("Row " + row.getData().id + " Clicked!!!!");
    },
  });
}

if (document.getElementById('accounts-table')) {
  table = new Tabulator("#accounts-table", {
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/account_list',
    columns: [ //Define Table Columns
      { title: "Id", field: "id" },
      { title: "name", field: "username", hozAlign: "left" },
      { title: "Email", field: "email" },
      { title: "Reseller", field: "reseller" },
      { title: "Created", field: "created_at", sorter: "date", hozAlign: "center" },
      { title: "Comment", field: "comment" },
    ],
    rowClick: function (e, row) { //trigger an alert message when the row is clicked
      alert("Row " + row.getData().id + " Clicked!!!!");
    },
  });
}