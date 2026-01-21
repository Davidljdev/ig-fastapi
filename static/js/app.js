
// Esto se ejecuta al cargar la página
window.addEventListener("DOMContentLoaded", () => {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0"); // meses empiezan en 0
    const dd = String(today.getDate()).padStart(2, "0");

    const todayStr = `${yyyy}-${mm}-${dd}`;
    document.getElementById("deleteDate").value = todayStr;
});

// -------------------
// PUT
// -------------------
async function addUrl() {
    const url = document.getElementById("urlInput").value;
    const result = document.getElementById("addResult");

    result.innerHTML = "";

    const res = await fetch("/urls", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    });

    const data = await res.json();
    //console.log(data);

    if (res.ok) {
        result.className = "result success";
        result.innerText = data.detail.message;
        document.getElementById("urlInput").value = "";
    } else {
        result.className = "result error";
        if (res.status == 422) {
            result.innerText = data.detail[0].msg
        }
        else {
            result.innerText = data.detail.message;
        }

    }
}

// -------------------
// GET
// -------------------
async function getUrls() {
    const includeDeleted = !document.getElementById("onlyActive").checked;
    const urlId = document.getElementById("idFilter").value;
    const tableContainer = document.getElementById("tableContainer");
    const table = document.getElementById("urlsTable");
    const noDataMessage = document.getElementById("noDataMessage");

    table.innerHTML = "";
    tableContainer.style.display = "none";
    noDataMessage.style.display = "none";

    let query = `?include_deleted=${includeDeleted}`;
    if (urlId) query += `&url_id=${urlId}`;

    try {
        const res = await fetch(`/urls${query}`);
        const data = await res.json();
        console.log("Datos recibidos:", data);

        // Asegurarse de que data sea un array
        const urls = Array.isArray(data) ? data : [];

        if (!urls.length) {
            noDataMessage.style.display = "block";
            return;
        }

        urls.forEach(row => {
            // Extraer solo el código final de la URL de Instagram
            let displayUrl = row.url;
            const reelIndex = row.url.indexOf("www.instagram.com/");
            if (reelIndex !== -1) {
                displayUrl = row.url.slice(reelIndex + "www.instagram.com/".length);
            }

            // Formatear fechas seguro sin microsegundos
            function formatDate(dateStr) {
                if (!dateStr) return "-";
                const [datePart, timePart] = dateStr.split('T'); // ISO8601
                const timeShort = timePart ? timePart.split('.')[0] : "";
                return `${datePart} ${timeShort}`;
            }

            const created = formatDate(row.created_at);
            const deleted = formatDate(row.deleted_at);

            table.innerHTML += `
                <tr>
                  <td>${row.id}</td>
                  <td>${displayUrl}</td>
                  <td>${created}</td>
                  <td>${deleted}</td>
                </tr>
            `;
        });

        tableContainer.style.display = "block";

    } catch (error) {
        noDataMessage.textContent = "An error occurred while querying the API.";
        noDataMessage.style.display = "block";
        console.error("Error al obtener datos:", error);
    }
}

// -------------------
// DEL
// -------------------
async function deleteUrls() {
    const date = document.getElementById("deleteDate").value;
    const id = document.getElementById("deleteId").value;
    const result = document.getElementById("deleteResult");

    if (!date) {
        result.className = "result error";
        result.innerText = "The date is required.";
        return;
    }

    let query = `?delete_date=${date}`;
    if (id) query += `&url_id=${id}`;

    const res = await fetch(`/urls${query}`, {
        method: "DELETE"
    });

    const data = await res.json();

    if (res.ok) {
        result.className = "result success";
        result.innerText = data.message;
    } else {
        result.className = "result error";
        result.innerText = data.detail;
    }
}