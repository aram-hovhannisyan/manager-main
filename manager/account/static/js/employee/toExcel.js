const exportButtons = document.querySelectorAll('[class^="export-Button"]');

exportButtons.forEach((button) => {
  const supplierId = button.className.match(/export-Button(\d+)/)[1];
  button.addEventListener('click', (event) => {
    const table = document.getElementById(supplierId);
    const today = new Date().toISOString().split('T')[0];
    const fileName = prompt("Enter the file name", `table_${today}.xlsx`);
    if (fileName) {
      exportToExcel(table, fileName);
      window.location.reload();
    }
  });
});

// Function to export table content to Excel and trigger download
function exportToExcel(table, fileName) {
  const rows = table.querySelectorAll('tbody tr');
  rows.forEach(row => {
    for (const el of row.children) {
      console.log(el);
        if (el.style.display === 'none'){
          row.removeChild(el)
        }
      }
    }
    )

  const wb = XLSX.utils.table_to_book(table);
  const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  const blob = new Blob([wbout], { type: "application/octet-stream" });

  // Check if the browser supports the download attribute
  if (typeof navigator.msSaveBlob !== "undefined") {
    // For IE and Edge browsers
    navigator.msSaveBlob(blob, fileName);
  } else {
    // For other browsers
    const link = document.createElement("a");
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", fileName);
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  }
}


