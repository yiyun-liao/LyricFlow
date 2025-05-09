import React from 'react';

function App() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/login";  // 觸發後端的 /login 路徑
  };

  return (
    <div className="App">
      <button onClick={handleLogin}>Login with Spotify</button>
    </div>
  );
}

export default App;
