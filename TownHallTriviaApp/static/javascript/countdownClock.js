// function getTimeRemaining(endtime){
//   var t = Date.parse(endtime) - Date.parse(new Date());
//   var seconds = Math.floor( (t/1000) % 60 );
//   var minutes = Math.floor( (t/1000/60) % 60 );
//   var hours = Math.floor( (t/(1000*60*60)) % 24 );
//   var days = Math.floor( t/(1000*60*60*24) );
//   return {
//     'total': t,
//     'days': days,
//     'hours': hours,
//     'minutes': minutes,
//     'seconds': seconds
//   };
// }

// function initializeClock(id, endtime){
//   var clock = document.getElementById(id);
//   var time = getTimeRemaining(endtime);
//     clock.innerHTML = 'days: ' + time.days + '<br>' +
//                       'hours: '+ time.hours + '<br>' +
//                       'minutes: ' + time.minutes + '<br>' +
//                       'seconds: ' + ('0' + time.seconds).slice(-2);
//   var timeinterval = setInterval(function(){
//     var t = getTimeRemaining(endtime);
//     clock.innerHTML = 'days: ' + t.days + '<br>' +
//                       'hours: '+ t.hours + '<br>' +
//                       'minutes: ' + t.minutes + '<br>' +
//                       'seconds: ' + ('0' + t.seconds).slice(-2);
//     // clock.innerHTML = 'seconds: ' + t.seconds;
//     if(t.total<=0){
//       clearInterval(timeinterval);
//     }
//   },1000);
// }

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
  var button = document.getElementById(buttonId);
  button.style.display = 'none';
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total <= 0) {
      clearInterval(timeinterval);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}


