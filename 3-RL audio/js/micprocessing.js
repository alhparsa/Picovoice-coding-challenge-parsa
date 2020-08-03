// inspired by https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
// Supports both firefox and chrome, for safari MediaRecorder must be enabled in experimental features menu.
const record = document.getElementById("record");
const stop = document.getElementById("stop");
const canvas = document.getElementById("drawingCanvas");
const canvasCtx = canvas.getContext("2d");
const WIDTH = 400;
const HEIGHT = 120;
var i = 0;

canvasCtx.clearRect(0, 0, 400, 120);

visiualize = async (blob) => {
  var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  var source = audioCtx.createBufferSource();
  var analyser = audioCtx.createAnalyser();
  var bufferLength;
  var dataArray;
  var songBuffer;

  // source.buffer = blob.arrayBuffer();

  songBuffer = await blob.arrayBuffer();

  source.buffer = await audioCtx.decodeAudioData(songBuffer);
  source.connect(analyser);
  analyser.connect(audioCtx.destination);
  analyser.fftSize = 2048;
  bufferLength = analyser.frequencyBinCount;
  dataArray = new Float32Array(bufferLength);
  temp = new Float32Array(bufferLength);
  setTimeout(function () {
    alert("Hello");
  }, 400);
  analyser.getFloatTimeDomainData(dataArray);
  for (var i = 0; i < bufferLength; i++) {
    if (temp[i] != dataArray[i]) {
      console.log(temp[i], dataArray[i]);
    }
  }
  // draw();

  function draw() {
    var drawVisual = requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArray);
    canvasCtx.fillStyle = "rgb(200, 200, 200)";
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);
    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = "rgb(0, 0, 0)";
    canvasCtx.beginPath();
    var sliceWidth = (WIDTH * 1.0) / bufferLength;
    var x = 0;
    for (var i = 0; i < bufferLength; i++) {
      var v = dataArray[i] / 128.0;
      var y = (v * HEIGHT) / 2.0;

      if (i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }
    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();
  }
};

// Recording audio
handleRecording = (stream) => {
  //   Creating a new instance of mediarecorder
  const mediaRecorder = new MediaRecorder(stream);
  var data = [];
  record.onclick = () => {
    mediaRecorder.start();
    record.disabled = true;
    stop.disabled = false;
  };
  mediaRecorder.ondataavailable = (e) => {
    data.push(e.data);
  };

  stop.onclick = () => {
    mediaRecorder.stop();
    record.disabled = false;
    stop.disabled = true;
  };
  // Stopping the recording and creating a playable stream
  mediaRecorder.onstop = (e) => {
    const audioClip = document.createElement("audio");
    audioClip.setAttribute("controls", "");
    const blob = new Blob(data, { type: "audio/mp3" });
    const audioURL = window.URL.createObjectURL(blob);
    audioClip.src = audioURL;
    audioClip.setAttribute("id", "recorded_audio" + i);
    audioClip.onplay = visiualize(blob);
    // audioClip.setAttribute("onplay", visiualize(e, stream));
    const audioRecordings = document.getElementById("recordings");
    audioRecordings.appendChild(audioClip);
    data = [];
  };
};

// if any devices are available for recording
if (navigator.mediaDevices || navigator.mediaDevices.getUserMedia) {
  // We only need audio, no video or anything
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then(handleRecording)
    .catch(function (err) {
      console.log("The following getUserMedia error occured: " + err);
    });
} else {
  console.log("getUserMedia not supported on your browser!");
}
