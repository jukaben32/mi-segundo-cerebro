import React from 'react';
import ScrollVideoBackground from './components/ScrollVideoBackground';
import ScrollFloat from './components/ScrollFloat';
import ContentStack from './components/ContentStack';

function App() {
  return (
    <div className="app">
      <ScrollVideoBackground frameCount={30} />
      
      <main>
        <ScrollFloat />
        <ContentStack />
        
        {/* Bottom Spacer to allow full scroll of the last panel */}
        <div style={{ height: '50vh' }} />
        
        <footer style={{ 
          padding: '4rem', 
          textAlign: 'center', 
          color: 'var(--text-muted)',
          borderTop: '1px solid rgba(255,255,255,0.1)'
        }}>
          Elite Cinematic Template &bull; 2026
        </footer>
      </main>
    </div>
  );
}

export default App;
