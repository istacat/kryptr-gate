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

if (document.getElementById('products-table')) {
  table = new Tabulator("#products-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/product_list',
    columns: [ //Define Table Columns
      { title: "Id", field: "id" },
      { title: "Product name", field: "name", hozAlign: "left" },
      { title: "Comment", field: "comment" },
    ],
    rowClick: function (e, row) { //trigger an alert message when the row is clicked
      alert("Row " + row.getData().id + " Clicked!!!!");
    },
  });
}

if (document.getElementById('users-table')) {
  table = new Tabulator("#users-table", {
    pagination:"remote", //enable remote pagination
    paginationSize:2, //optional parameter to request a certain number of rows per page
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + `/api/user_list` ,
    paginationDataReceived:{
      "last_page":"max_pages", //change last_page parameter name to "max_pages"
  } ,
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
if (document.getElementById('sub_resellers-table')) {
  table = new Tabulator("#sub_resellers-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/sub_reseller_list',
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

if (document.getElementById('resellers-table')) {
  table = new Tabulator("#resellers-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/reseller_list',
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
if (document.getElementById('distributors-table')) {
  table = new Tabulator("#distributors-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/distributor_list',
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
    pagination:"local", //enable remote pagination
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + '/api/account_list',
    paginationSize:30, //optional parameter to request a certain number of rows per page
    paginationInitialPage:20, //optional parameter to set the initial page to load
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
//   table.setFilter([
//     {field:"id", type:">", value:260}, //filter by age greater than 52
// ]);
}