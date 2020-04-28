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

function autoDisableRound(clockId, roundId, endTime) {
    if (Date.parse(endTime) > Date.parse(new Date())) {
        console.log("in js. autoDisableRound")
        var clock = document.getElementById(clockId);
        clock.style.display = 'block';
        var minutesSpan = clock.querySelector('.minutes');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(endTime);

            minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);
            if (t.minutes <= 0 && t.seconds <= 0) {
                $.post("toggleRound",
                    {
                        submit: "Disabled",
                        roundId: roundId
                    },
                    function(data,status){ 
                        var message = document.getElementById("message");
                        message.innerHTML = "Disabled " + roundId;
                        console.log(window.location.href )
                        location.assign(window.location.href)
                    });
                clearInterval(timeinterval);
            }
        }

        updateClock();
        var timeinterval = setInterval(updateClock, 1000);
    }
}


