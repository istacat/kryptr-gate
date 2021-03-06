const menuBtn = document.querySelector(".menu-btn");
const menu = document.querySelector(".menu");
const overlay = document.querySelector(".overlay");

menuBtn &&
  menuBtn.addEventListener("click", function () {
    menuBtn.classList.toggle("menu-btn--active");
    menu.classList.toggle("menu--active");
    overlay.classList.toggle("overlay--active");
  });

function showFuncs() {
  document.getElementById("funcs-drp").classList.toggle("show");
}

overlay &&
  overlay.addEventListener("click", function () {
    menuBtn.classList.toggle("menu-btn--active");
    menu.classList.toggle("menu--active");
    overlay.classList.toggle("overlay--active");
  });
const printIcon = function (cell, formatterParams, onRendered) {
  //plain text value
  return "<div class='icon__delete' >&#10008</div>";
};
const printIconView = function (cell, formatterParams, onRendered) {
  //plain text value
  return "<div class='qrcode-container'><img src='static/images/icons/qrcode.svg' class='qrcode-icon' ></img></div>";
};
if (document.getElementById("products-table")) {
  table = new Tabulator("#products-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + "/api/product_list",
    columns: [
      //Define Table Columns
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " + cell.getRow().getData().name
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_product?id=" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Product name", field: "name", hozAlign: "left" },
      { title: "Comment", field: "comment" },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_product?id=" + row.getData().id;
    },
  });
}

if (document.getElementById("users-table")) {
  table = new Tabulator("#users-table", {
    responsiveLayout: "collapse",
    pagination: "local", //enable remote pagination
    paginationSize: 20, //optional parameter to request a certain number of rows per page
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + "/api/user_list",
    columns: [
      //Define Table Columns
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " +
                cell.getRow().getData().username
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_user/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Username", field: "username", hozAlign: "left", minWidth: 360 },
      { title: "Email", field: "email", minWidth: 160 },
      { title: "Activated", field: "activated", minWidth: 160 },
      { title: "Role", field: "role", minWidth: 160 },
      {
        title: "Created",
        field: "created_at",
        sorter: "date",
        hozAlign: "center",
        minWidth: 160,
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_user/" + row.getData().id;
    },
  });
}
if (document.getElementById("sub_resellers-table")) {
  table = new Tabulator("#sub_resellers-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + "/api/sub_reseller_list",
    columns: [
      //Define Table Columns
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " +
                cell.getRow().getData().username
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_sub_reseller/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Username", field: "username", hozAlign: "left" },
      { title: "Email", field: "email" },
      { title: "Activated", field: "activated" },
      { title: "Role", field: "role" },
      {
        title: "Created",
        field: "created_at",
        sorter: "date",
        hozAlign: "center",
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_sub_reseller/" + row.getData().id;
    },
  });
}

if (document.getElementById("resellers-table")) {
  table = new Tabulator("#resellers-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + "/api/reseller_list",
    columns: [
      //Define Table Columns
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " +
                cell.getRow().getData().username
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_reseller/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Username", field: "username", hozAlign: "left" },
      { title: "Email", field: "email" },
      { title: "Activated", field: "activated" },
      { title: "Role", field: "role" },
      {
        title: "Created",
        field: "created_at",
        sorter: "date",
        hozAlign: "center",
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_reseller/" + row.getData().id;
    },
  });
}
if (document.getElementById("distributors-table")) {
  table = new Tabulator("#distributors-table", {
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + "/api/distributor_list",
    columns: [
      //Define Table Columns
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " +
                cell.getRow().getData().username
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_distributor/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Username", field: "username", hozAlign: "left" },
      { title: "Email", field: "email" },
      { title: "Activated", field: "activated" },
      { title: "Role", field: "role" },
      {
        title: "Created",
        field: "created_at",
        sorter: "date",
        hozAlign: "center",
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_distributor/" + row.getData().id;
    },
  });
}

if (document.getElementById("accounts-table")) {
  //Define variables for input elements
  var valueEl = document.getElementById("filter-value");

  //Trigger setFilter function with correct parameters
  function updateFilter() {
    var typeVal = "like";

    var filter = "ecc_id";
    var filterVal = true;

    if (filterVal) {
      table.setFilter(filter, typeVal, valueEl.value);
    }
  }

  //Update filters on value change

  document
    .getElementById("filter-value")
    .addEventListener("keyup", updateFilter);

  table = new Tabulator("#accounts-table", {
    resizableColumns: false,
    responsiveLayout: "collapse",
    pagination: "remote", //enable remote pagination
    layout: "fitColumns",
    ajaxURL: window.location.origin + "/api/account_list",
    ajaxFiltering: true,
    headerSort: false,
    paginationSize: 20, //optional parameter to request a certain number of rows per page

    columns: [
      { title: "Id", field: "id" },
      { title: "Ecc id", field: "ecc_id", widthGrow: 2},
      { title: "Activation date", field: "activation_date", widthGrow: 5 },
      { title: "Expiration date", field: "expiration_date", widthGrow: 5 },
      {
        field: "actions",
        formatter: printIconView,
        widthGrow: 1,
        headerSort: false,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          window.location.href =
            window.location.origin + "/qrcode/" + cell.getRow().getData().id;
        },
      },
      {
        field: "actions",
        formatter: printIcon,
        widthGrow: 1,
        hozAlign: "center",
        headerSort: false,
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " + cell.getRow().getData().name
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_account/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_account/" + row.getData().id;
    },
  });
}

if (document.getElementById("supports-table")) {
  table = new Tabulator("#supports-table", {
    responsiveLayout: "collapse",
    pagination: "remote", //enable remote pagination
    paginationSize: 20, //optional parameter to request a certain number of rows per page
    // height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout: "fitColumns", //fit columns to width of table (optional)
    ajaxURL: window.location.origin + `/api/support_list`,
    paginationDataReceived: {
      last_page: "max_pages", //change last_page parameter name to "max_pages"
    },
    columns: [
      //Define Table Columns
      {
        formatter: "responsiveCollapse",
        width: 30,
        minWidth: 30,
        align: "center",
        resizable: false,
        headerSort: false,
      },
      { title: "Id", field: "id" },
      {
        field: "actions",
        minWidth: 50,
        formatter: printIcon,
        width: 20,
        hozAlign: "center",
        cellClick: function (e, cell) {
          e.stopPropagation();
          if (
            confirm(
              "Are you sure you want to delete " +
                cell.getRow().getData().username
            )
          ) {
            window.location.href =
              window.location.origin +
              "/delete_support/" +
              cell.getRow().getData().id;
          } else return;
        },
      },
      { title: "Username", field: "username", hozAlign: "left", minWidth: 166 },
      { title: "Email", field: "email", minWidth: 166 },
      { title: "Activated", field: "activated", minWidth: 166 },
      { title: "Role", field: "role", minWidth: 166 },
      {
        title: "Created",
        field: "created_at",
        sorter: "date",
        hozAlign: "center",
        minWidth: 166,
      },
    ],
    rowClick: function (e, row) {
      window.location.href =
        window.location.origin + "/edit_support/" + row.getData().id;
    },
  });
}

const closeBtn = document.getElementById("close-btn");
if (closeBtn) {
  closeBtn.addEventListener("click", function (e) {
    document.getElementById("alert").hidden = true;
  });
}
