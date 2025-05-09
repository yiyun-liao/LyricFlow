'use client';

export default function Page() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/login"; // 導向 FastAPI 的 /login
  };

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Spotify Lyrics Translator</h1>
      <button onClick={handleLogin}>Login with Spotify</button>
    </main>
  );
}
