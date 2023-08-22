let isTimerStarted = false; // Boolean flag to track if the timer is started
let startTime = 0; // Variable to store the start time of the timer

function start() {
  startTime = performance.now(); // Store the start time when the timer starts
  cron = setInterval(() => {
    timer();
  }, 1); // Update the timer every millisecond
}

function timer() {
  const currentTime = performance.now();
  const elapsedTime = currentTime - startTime;

  let millisecond = Math.floor(elapsedTime % 1000);
  let second = Math.floor((elapsedTime / 1000) % 60);
  let minute = Math.floor((elapsedTime / 60000) % 60);
  let hour = Math.floor(elapsedTime / 3600000);

  document.getElementById("hour").innerText = returnData(hour);
  document.getElementById("minute").innerText = returnData(minute);
  document.getElementById("second").innerText = returnData(second);
  document.getElementById("millisecond").innerText = returnData(millisecond);
  document.getElementById("durationInput").value = `${returnData(hour)}:${returnData(minute)}:${returnData(second)}`;

}

function returnData(input) {
  return input > 10 ? input : `0${input}`;
}

function startTimer() {
  if (!isTimerStarted) {
    start();
    isTimerStarted = true;
  }
}


