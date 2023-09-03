const userForm = document.querySelector("#userForm");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/usuarios");
  const data = await response.json();
  users = data;
  renderUser(users);
});

userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const cedula_identidad = userForm["cedula_identidad"].value;
  const nombre = userForm["nombre"].value;
  const primer_apellido = userForm["primer_apellido"].value;
  const segundo_apellido = userForm["segundo_apellido"].value;
  const fecha_nacimiento = userForm["fecha_nacimiento"].value;

  if (!editing) {
    const response = await fetch("/api/usuarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cedula_identidad,
        nombre,
        primer_apellido,
        segundo_apellido,
        fecha_nacimiento,
      }),
    });

    const data = await response.json();
    users.push(data);
    renderUser(users);
  } else {
    const response = await fetch(`/api/usuarios/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cedula_identidad,
        nombre,
        primer_apellido,
        segundo_apellido,
        fecha_nacimiento,
      }),
    });
    const updatedUser = await response.json();

    users = users.map((user) =>
      user.id === updatedUser.id ? updatedUser : user
    );
    console.log(users)
    renderUser(users);

    editing = false;
    userId = null;
  }
  userForm.reset();
});

function renderUser(users) {
  const userList = document.querySelector("#userList");
  userList.innerHTML = "";
  users.forEach((user) => {
    const userItem = document.createElement("li");
    userItem.classList = "table-responsive";
    userItem.innerHTML = `
    <table id="datatable" class="table-bordered border table table-striped dataTable p-0">
        <thead>
        <tr>
          <th>Nombre</th>
          <th>Paterno</th>
          <th>Materno</th>
          <th>Fecha Nacimiento</th>
          <th>Modificar</th>
          <th>Eliminar</th>
        </tr>
      </thead>

        <tbody>
          <tr>
            <td>${user.nombre}</td>
            <td>${user.primer_apellido}</td>
            <td>${user.segundo_apellido}</td>
            <td>${user.fecha_nacimiento}</td>
            <td>
              <button data-id="${user.id}" class="btn-delete btn btn-danger btn-sm">Delete</button>
            </td>
            <td>
              <button data-id="${user.id}" class="btn-edit btn btn-secondary btn-sm">Edit</button>
            </td>
          </tr>
        </tbody>
        </table>
    `;
    const btnDelete = userItem.querySelector(".btn-delete");

    btnDelete.addEventListener("click", async (e) => {
      const response = await fetch(`/api/usuarios/${user.id}`, {
        method: "DELETE",
      });

      const data = await response.json();

      users = users.filter((user) => user.id !== data.id);
      renderUser(users);
    });

    userList.appendChild(userItem);

    // Handle edit button
    const btnEdit = userItem.querySelector(".btn-edit");

    btnEdit.addEventListener("click", async (e) => {
      const response = await fetch(`/api/usuarios/${user.id}`);
      const data = await response.json();

      userForm["cedula_identidad"].value = data.cedula_identidad;
      userForm["nombre"].value = data.nombre;
      userForm["primer_apellido"].value = data.primer_apellido;
      userForm["segundo_apellido"].value = data.segundo_apellido;
      userForm["fecha_nacimiento"].value = data.fecha_nacimiento;

      editing = true;
      userId = user.id;
    });
  });
}
