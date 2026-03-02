function getUsers() {
  //fetch('http://192.168.80.3:5002/api/users')
  fetch("http://192.168.80.3:5002/api/users", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle data
      console.log(data);

      // Get table body
      var userListBody = document.querySelector("#user-list tbody");
      userListBody.innerHTML = ""; // Clear previous data

      // Loop through users and populate table rows
      data.forEach((user) => {
        var row = document.createElement("tr");

        // Name
        var nameCell = document.createElement("td");
        nameCell.textContent = user.name;
        row.appendChild(nameCell);

        // Email
        var emailCell = document.createElement("td");
        emailCell.textContent = user.email;
        row.appendChild(emailCell);

        // Username
        var usernameCell = document.createElement("td");
        usernameCell.textContent = user.username;
        row.appendChild(usernameCell);

        // Actions
        var actionsCell = document.createElement("td");

        // Edit link
        var editLink = document.createElement("a");
        editLink.href = `/editUser/${user.id}`;
        //editLink.href = `edit.html?id=${user.id}`;
        editLink.textContent = "Edit";
        editLink.className = "btn btn-primary mr-2";
        actionsCell.appendChild(editLink);

        // Delete link
        var deleteLink = document.createElement("a");
        deleteLink.href = "#";
        deleteLink.textContent = "Delete";
        deleteLink.className = "btn btn-danger";
        deleteLink.addEventListener("click", function () {
          deleteUser(user.id);
        });
        actionsCell.appendChild(deleteLink);

        row.appendChild(actionsCell);

        userListBody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function createUser() {
  var data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
  };

  fetch("http://192.168.80.3:5002/api/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Handle success
      console.log(data);
      // Limpiar el formulario
      document.getElementById("name").value = "";
      document.getElementById("email").value = "";
      document.getElementById("username").value = "";
      document.getElementById("password").value = "";
      alert("Usuario creado exitosamente");
      getUsers();
    })
    .catch((error) => {
      // Handle error
      console.error("Error:", error);
    });
}

function updateUser() {
  var userId = document.getElementById("user-id").value;
  var data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
  };

  fetch(`http://192.168.80.3:5002/api/users/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Handle success
      console.log(data);
      // Optionally, redirect to another page or show a success message
    })
    .catch((error) => {
      // Handle error
      console.error("Error:", error);
    });
}

function deleteUser(userId) {
  console.log("Deleting user with ID:", userId);
  if (confirm("Are you sure you want to delete this user?")) {
    fetch(`http://192.168.80.3:5002/api/users/${userId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Handle success
        console.log("User deleted successfully:", data);
        // Reload the user list
        getUsers();
      })
      .catch((error) => {
        // Handle error
        console.error("Error:", error);
      });
  }
}

function handleLogin(event) {
  //event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch("http://192.168.80.3:5002/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid credentials");
      }
      return response.json();
    })
    .then((data) => {
      // Obtener datos del usuario para luego usarlos en órdenes
      fetch("http://192.168.80.3:5002/api/users", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      })
        .then((response) => response.json())
        .then((users) => {
          // Buscar el usuario que coincide con el username
          const loggedUser = users.find((u) => u.username === username);
          if (loggedUser) {
            // Guardar datos del usuario en sessionStorage
            sessionStorage.setItem("username", loggedUser.username);
            sessionStorage.setItem("email", loggedUser.email);
            sessionStorage.setItem("user_id", loggedUser.id);
            sessionStorage.setItem("name", loggedUser.name);
          }
          // Redirect to the desired page after successful login
          window.location.href = "/dashboard";
        })
        .catch((error) => {
          console.error("Error obteniendo datos del usuario:", error);
          window.location.href = "/dashboard";
        });
    })
    .catch((error) => {
      console.error("Login error:", error);
      // Display an error message to the user
      alert("Invalid credentials");
    });
}

//const loginForm = document.getElementById('login-form');
//loginForm.addEventListener('submit', handleLogin);
