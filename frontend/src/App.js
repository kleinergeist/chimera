import { SignedIn, SignedOut, useUser } from '@clerk/clerk-react';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  const { isLoaded } = useUser();

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <SignedOut>
        <LandingPage />
      </SignedOut>

      <SignedIn>
        <Dashboard />
      </SignedIn>
    </div>
  );
}

export default App;
