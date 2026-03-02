function getOrders() {
  fetch("http://192.168.80.3:5004/api/orders", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      var tbody = document.querySelector("#order-list tbody");
      tbody.innerHTML = "";

      data.forEach((order) => {
        var row = document.createElement("tr");

        row.innerHTML = `
          <td>${order.id}</td>
          <td>${order.user_name}</td>
          <td>${order.user_email}</td>
          <td>$${order.total.toFixed(2)}</td>
          <td>${new Date(order.created_at).toLocaleString()}</td>
          <td>
            <a href="/editOrder/${order.id}" class="btn btn-primary mr-2">View</a>
            <a href="#" class="btn btn-danger" onclick="deleteOrder(${order.id})">Delete</a>
          </td>
        `;

        tbody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function getOrder(orderId) {
  fetch(`http://192.168.80.3:5004/api/orders/${orderId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((order) => {
      document.getElementById("user-name").value = order.user_name;
      document.getElementById("user-email").value = order.user_email;
      document.getElementById("total").value = `$${order.total.toFixed(2)}`;
      document.getElementById("created-at").value = new Date(
        order.created_at,
      ).toLocaleString();

      var tbody = document.querySelector("#items-table tbody");
      tbody.innerHTML = "";

      order.items.forEach((item) => {
        var row = document.createElement("tr");
        row.innerHTML = `
          <td>${item.product_id}</td>
          <td>${item.quantity}</td>
          <td>$${item.price.toFixed(2)}</td>
          <td>$${item.subtotal.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function deleteOrder(orderId) {
  if (confirm("¿Estás seguro de que deseas eliminar esta orden?")) {
    fetch(`http://192.168.80.3:5004/api/orders/${orderId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Orden eliminada:", data);
        getOrders();
      })
      .catch((error) => console.error("Error:", error));
  }
}
