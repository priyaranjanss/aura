import Sidebar from './components/Sidebar';
import Home from './pages/Home';

export default function App() {
  return (
    <div className="flex h-screen overflow-hidden bg-aura-bg text-white">
      <Sidebar />
      <Home />
    </div>
  );
}
