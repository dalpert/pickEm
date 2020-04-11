/// Create and download a csv file given an html form.
function DownloadCsv(form) {
  // Create table data from form responses
  table = [];
  var teamName = form.TeamName.value;

  // Create CSV file
  const exporter = new TableCSVExporter(table);
  const csvOutput = exporter.ConvertToCSV();

  // Download csv
  var hiddenElement = document.createElement('a');
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvOutput);
  hiddenElement.target = '_blank';
  hiddenElement.download = form.TeamName.value + '.csv';
  hiddenElement.click();

  // Save CSV
  
}