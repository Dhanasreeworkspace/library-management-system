async function loadDashboard() {

    const response = await fetch(
        "http://127.0.0.1:8018/api/method/library_management.library.api.dashboard.get_dashboard_data"
    );

    const result = await response.json();

    document.getElementById("totalBooks").innerText =
        result.message.total_books;

    document.getElementById("availableBooks").innerText =
        result.message.available_books;

    document.getElementById("issuedBooks").innerText =
        result.message.issued_books;

    document.getElementById("members").innerText =
        result.message.members;

    document.getElementById("overdueBooks").innerText =
        result.message.overdue_books;
}

loadDashboard();