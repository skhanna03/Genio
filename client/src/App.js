import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);  // State for member data
  const [text, setText] = useState('');  // State for text input
  const [videoUrl, setVideoUrl] = useState(null);  // State for local video URL
  const [audioFile, setAudioFile] = useState(null);  // State for received audio file URL

  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data);
        console.log(data);
      }
    )
  }, []);

  const handleVideoChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoUrl(URL.createObjectURL(file)); // Create and set local URL for the video
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('text', text);

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAudioFile(response.data.audioFile);
    } catch (error) {
      console.error('Error processing text', error);
    }
  };

  return (
    <div>
      {/* Displaying members */}
      {data ? (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      ) : (
        <p>Loading...</p>
      )}

      {/* Video upload and display */}
      <input type="file" accept="video/*" onChange={handleVideoChange} />
      {videoUrl && (
        <div>
          <video src={videoUrl} controls autoPlay style={{ width: '100%', maxHeight: '500px' }} />
          <button onClick={() => setVideoUrl(null)}>Clear Video</button>
        </div>
      )}

      {/* Text input and submit */}
      <form onSubmit={handleSubmit}>
        <input type="text" value={text} onChange={(e) => setText(e.target.value)} />
        <button type="submit">Submit</button>
      </form>

      {/* Audio playback */}
      {audioFile && <audio src={audioFile} controls autoPlay />}
    </div>
  );
}

export default App;
