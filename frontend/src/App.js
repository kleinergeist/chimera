import { SignedIn, SignedOut, useUser } from '@clerk/clerk-react';
import NewLandingPage from './pages/NewLandingPage';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  const { isLoaded } = useUser();

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <SignedOut>
        <NewLandingPage />
      </SignedOut>

      <SignedIn>
        <Dashboard />
      </SignedIn>
    </div>
  );
}

export default App;
