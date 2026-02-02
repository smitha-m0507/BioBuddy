function toggleDetails(id) {
    let detailsRow = document.getElementById(id);
    if (detailsRow.style.display === "none" || detailsRow.style.display === "") {
        detailsRow.style.display = "table-row"; // Show details
    } else {
        detailsRow.style.display = "none"; // Hide details
    }
}

function openPDF(pdfFile) {
    window.open(pdfFile, "_blank"); // Opens the PDF in a new tab
}
