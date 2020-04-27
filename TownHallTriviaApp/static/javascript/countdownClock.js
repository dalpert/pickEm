function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  return {
    'total': t,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(clockId, buttonId, endtime) {
  var clock = document.getElementById(clockId);
  clock.style.display = 'block';
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.minutes <= 0 && t.seconds <= 0) {
      document.getElementById("roundForm").submit();
      clearInterval(timeinterval);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}


