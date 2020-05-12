function validateForm() {
  var date = document.forms["registerForNextWeek"]["date"].value;
  console.log(date)
  if (!isValidDate(date)) {
    alert('Invalid date format! Must be in the form: yyyy-mm-dd AND it must be a Wednseday.');
    document.registerForNextWeek.date.focus();
    return false;
  }
}

function isValidDate(dateString) {
	// yyyy-mm-dd
  	var regEx = /^\d{4}-\d{2}-\d{2}$/;
  	if(!dateString.match(regEx)) return false;  // Invalid format
  	var d = new Date(dateString);
  	console.log("LOGGING DAY OF THE WEEK::")
  	var dNum = d.getTime();
  	if(!dNum && dNum !== 0) return false; // NaN value, Invalid date
  	return d.toISOString().slice(0,10) === dateString && d.getDay() == 2;
}
