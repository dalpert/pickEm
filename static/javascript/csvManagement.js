//////////////////////////////////////////
/// File to help manage CSV operations ///
//////////////////////////////////////////

class TableCSVExporter {
  /// Constructor.
  constructor(table) {
    this.headerRow = table[0];
    this.numColumns = this.headerRow.length
    this.rows = table;
    this.rows.shift();
  }

  /// Convert JS table to csv.
  ConvertToCSV() {
    const csv = [];
    csv.push(this.headerRow);

    for (const answers of this.rows) {
      csv.push(this.CleanAnswers(answers));
    }

    return csv.join("\n");
  }

  /// Clean answers.
  CleanAnswers(answers) {
    let cleansedAnswers = [];

    for (let i = 0; i < this.numColumns; i++) {
      if (answers[i] !== undefined)
      {
        cleansedAnswers.push(TableCSVExporter.ParseCell(answers[i]));
      }
      else 
      {
        cleansedAnswers.push("Couldn't Read Answer");
      }
    }

    return cleansedAnswers.join();
  }

  /// Cleanse cell of potentially harmful characters.
  static ParseCell(tableCell) {
    let parsedValue = tableCell;

    // Replace all double quotes with two double quotes
    // parsedValue = parsedValue.replace(/"/g, `""`);

    // If value contains comma, new-line or double-quote, enclose in double quotes
    // parsedValue = /[",\n]/.test(parsedValue) ? `"${parsedValue}"` : parsedValue;
    parsedValue = `"${parsedValue}"`;

    return parsedValue;
  }
}

/// Create and download a csv file given an html form.
function DownloadCsv(form) {
  // Create table header
  headerRow = [];
  headerRow.push("Timestamp");
  for (let i = 1; i < 7; i++) {
    headerRow.push("Question " + i.toString());
  }

  // Create table data from form responses
  table = [];
  var data = [new Date(), form.Question1.value, form.Question2.value,form.Question3.value,
              form.Question4.value, form.Question5.value, form.Question6.value];
  table.push(headerRow);
  table.push(data);

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