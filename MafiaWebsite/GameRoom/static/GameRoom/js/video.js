
// const SimplePeer = require('simple-peer');
// const video = document.getElementById('video');
//         const startButton = document.getElementById('startButton');
//         const stopButton = document.getElementById('stopButton');
//         const audio = document.getElementById('audio');

//         let stream = null;
//         let mediaRecorder = null;
//         let audioChunks = [];

//         startButton.addEventListener('click', () => {
//             startCapture();
//         });

//         stopButton.addEventListener('click', () => {
//             stopCapture();
//         });

//         async function startCapture() {
//             try {
//                 stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
//                 video.srcObject = stream;
//                 mediaRecorder = new MediaRecorder(stream);

//                 mediaRecorder.ondataavailable = (e) => {
//                     if (e.data.size > 0) {
//                         audioChunks.push(e.data);
//                     }
//                 };

//                 mediaRecorder.onstop = () => {
//                     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//                     audio.src = URL.createObjectURL(audioBlob);
//                 };

//                 mediaRecorder.start();
//                 startButton.disabled = true;
//                 stopButton.disabled = false;
//             } catch (error) {
//                 console.error('Error starting capture:', error);
//             }
//         }

//         function stopCapture() {
//             if (mediaRecorder && mediaRecorder.state === 'recording') {
//                 mediaRecorder.stop();
//                 stream.getTracks().forEach((track) => track.stop());
//                 startButton.disabled = false;
//                 stopButton.disabled = true;
//             }
//         }