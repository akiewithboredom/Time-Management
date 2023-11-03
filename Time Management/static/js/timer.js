window.onload = () => {
    document.querySelector('#start').onclick = startTimer;
    document.querySelector('#reset').onclick = resetTimer;
}

let interval;

function startTimer() {
    const timerLength = parseInt(document.querySelector("#timerLength").value);
    if (!timerLength || timerLength < 1) {
        alert("Please enter a valid timer length (minutes).");
        return;
    }
    
    const timerHours = document.querySelector("#countdown-hours");
    const timerMinutes = document.querySelector("#countdown-minutes");
    const timerSeconds = document.querySelector("#countdown-seconds");
    
    let totalSeconds = timerLength * 60;
    
    if (interval) {
        clearInterval(interval);
    }

    interval = setInterval(() => {
        if (totalSeconds <= 0) {
            clearInterval(interval);
            playSound(); // Call the function to play the sound
            timerHours.innerText = "00";
            timerMinutes.innerText = "00";
            timerSeconds.innerText = "00"
            return;
        }
        
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        timerHours.innerText = hours < 10 ? `0${hours}` : hours;
        timerMinutes.innerText = minutes < 10 ? `0${minutes}` : minutes;
        timerSeconds.innerText = seconds < 10 ? `0${seconds}` : seconds;

        totalSeconds--;
    }, 1000);
}

function playSound() {
    const alarm = document.getElementById("alarm");
    alarm.play();
}

function resetTimer() {
    clearInterval(interval);
    document.querySelector("#timerLength").value = "25";
    document.querySelector("#countdown-hours").innerText = "00";
    document.querySelector("#countdown-minutes").innerText = "00";
    document.querySelector("#countdown-seconds").innerText = "00";
}
