import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);  // State for member data
  const [text, setText] = useState('');  // State for text input
  const [videoFile, setVideoFile] = useState(null);  // State for video file
  const [audioFile, setAudioFile] = useState(null);  // State for received audio file

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('text', text);
    formData.append('video', videoFile);

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAudioFile(response.data.audioFile);
    } catch (error) {
      console.error('Error uploading files', error);
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

      {/* File upload form */}
      <form onSubmit={handleSubmit}>
        <input type="text" value={text} onChange={(e) => setText(e.target.value)} />
        <input type="file" onChange={(e) => setVideoFile(e.target.files[0])} />
        <button type="submit">Submit</button>
      </form>
      {audioFile && <audio src={audioFile} controls />}
      <button onClick={() => {/* Function to trigger download */}}>Download Merged Video</button>
    </div>
  );
}

export default App;