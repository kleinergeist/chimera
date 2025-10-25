import { SignedIn, SignedOut, SignIn, SignUp, UserButton, useUser, useAuth } from '@clerk/clerk-react';
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const { user, isLoaded } = useUser();
  const { getToken } = useAuth();
  const [userData, setUserData] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [buckets, setBuckets] = useState([]);
  const [showSignUp, setShowSignUp] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      fetchUserData();
      fetchSessions();
      fetchBuckets();
    }
  }, [user]);

  const fetchUserData = async () => {
    setLoading(true);
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setUserData(data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSessions = async () => {
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/sessions`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchBuckets = async () => {
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/buckets`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setBuckets(data.buckets || []);
    } catch (error) {
      console.error('Error fetching buckets:', error);
    }
  };

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
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8 items-center">
            {/* Left side - Hero content */}
            <div className="text-center md:text-left space-y-6">
              <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Chimera
              </h1>
              <p className="text-2xl text-gray-700">
                Discover, organize, and manage your digital accounts
              </p>
              <p className="text-lg text-gray-600">
                A modern platform for account discovery and intelligent categorization
              </p>
              <div className="flex gap-4 justify-center md:justify-start">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600">Secure</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600">Fast</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600">Intuitive</span>
                </div>
              </div>
            </div>

            {/* Right side - Auth */}
            <div className="flex justify-center">
              <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
                {!showSignUp ? (
                  <div className="space-y-4">
                    <h2 className="text-2xl font-bold text-gray-800 text-center">Welcome Back</h2>
                    <SignIn 
                      appearance={{
                        elements: {
                          rootBox: "w-full",
                          card: "shadow-none"
                        }
                      }}
                    />
                    <p className="text-center text-sm text-gray-600">
                      Don't have an account?{' '}
                      <button 
                        onClick={() => setShowSignUp(true)}
                        className="text-blue-600 hover:text-blue-700 font-semibold"
                      >
                        Sign up
                      </button>
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <h2 className="text-2xl font-bold text-gray-800 text-center">Create Account</h2>
                    <SignUp 
                      appearance={{
                        elements: {
                          rootBox: "w-full",
                          card: "shadow-none"
                        }
                      }}
                    />
                    <p className="text-center text-sm text-gray-600">
                      Already have an account?{' '}
                      <button 
                        onClick={() => setShowSignUp(false)}
                        className="text-blue-600 hover:text-blue-700 font-semibold"
                      >
                        Sign in
                      </button>
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </SignedOut>

      <SignedIn>
        <div className="min-h-screen">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Chimera
                  </h1>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                    BETA
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-600">
                    {user?.firstName || user?.emailAddresses[0].emailAddress}
                  </span>
                  <UserButton afterSignOutUrl="/" />
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <div className="space-y-8">
                {/* Welcome Section */}
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl shadow-lg p-8 text-white">
                  <h2 className="text-3xl font-bold mb-2">
                    Welcome back, {user?.firstName || 'there'}!
                  </h2>
                  <p className="text-blue-100">
                    Your account discovery dashboard is ready
                  </p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Total Sessions</p>
                        <p className="text-3xl font-bold text-gray-800">{sessions.length}</p>
                      </div>
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Buckets</p>
                        <p className="text-3xl font-bold text-gray-800">{buckets.length}</p>
                      </div>
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Account ID</p>
                        <p className="text-3xl font-bold text-gray-800">{userData?.id}</p>
                      </div>
                      <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                {/* User Info Card */}
                <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">Account Information</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Email</p>
                      <p className="text-gray-800 font-medium">{userData?.email}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Member Since</p>
                      <p className="text-gray-800 font-medium">
                        {userData?.created_at ? new Date(userData.created_at).toLocaleDateString() : 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Database ID</p>
                      <p className="text-gray-800 font-medium">{userData?.id}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Clerk ID</p>
                      <p className="text-gray-800 font-medium text-xs">{userData?.clerk_id}</p>
                    </div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button className="px-6 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg">
                      Start New Session
                    </button>
                    <button className="px-6 py-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg">
                      Create Bucket
                    </button>
                    <button className="px-6 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-md hover:shadow-lg">
                      View Reports
                    </button>
                  </div>
                </div>
              </div>
            )}
          </main>
        </div>
      </SignedIn>
    </div>
  );
}

export default App;

