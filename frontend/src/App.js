import { SignedIn, SignedOut, SignIn, SignUp, UserButton, useUser, useAuth } from '@clerk/clerk-react';
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const { user, isLoaded } = useUser();
  const { getToken } = useAuth();
  const [userData, setUserData] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [buckets, setBuckets] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [showSignUp, setShowSignUp] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedBucket, setSelectedBucket] = useState(null);
  const [editingAccount, setEditingAccount] = useState(null);
  const [showNewBucketForm, setShowNewBucketForm] = useState(false);
  const [newBucketName, setNewBucketName] = useState('');
  const [newBucketDescription, setNewBucketDescription] = useState('');
  const [showSearchForm, setShowSearchForm] = useState(false);
  const [searchUsername, setSearchUsername] = useState('');
  const [searching, setSearching] = useState(false);
  const [searchResult, setSearchResult] = useState(null);

  useEffect(() => {
    if (user) {
      fetchUserData();
      fetchSessions();
      fetchBuckets();
      fetchAccounts();
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

  const fetchAccounts = async () => {
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/accounts`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setAccounts(data.accounts || []);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const updateAccountBucket = async (accountId, bucketId) => {
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/accounts/${accountId}/bucket`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bucket_id: bucketId })
      });
      
      if (response.ok) {
        fetchAccounts();
        setEditingAccount(null);
      }
    } catch (error) {
      console.error('Error updating account bucket:', error);
    }
  };

  const createBucket = async () => {
    if (!newBucketName.trim()) return;
    
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/buckets`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bucket_name: newBucketName,
          description: newBucketDescription
        })
      });
      
      if (response.ok) {
        fetchBuckets();
        setShowNewBucketForm(false);
        setNewBucketName('');
        setNewBucketDescription('');
      }
    } catch (error) {
      console.error('Error creating bucket:', error);
    }
  };

  const deleteBucket = async (bucketId) => {
    if (!window.confirm('Are you sure you want to delete this bucket? Accounts will be unassigned.')) return;
    
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/buckets/${bucketId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        fetchBuckets();
        fetchAccounts();
        if (selectedBucket === bucketId) {
          setSelectedBucket(null);
        }
      }
    } catch (error) {
      console.error('Error deleting bucket:', error);
    }
  };

  const searchAccounts = async () => {
    if (!searchUsername.trim()) return;
    
    setSearching(true);
    setSearchResult(null);
    
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/search-accounts`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: searchUsername })
      });
      
      if (response.ok) {
        const data = await response.json();
        setSearchResult(data);
        fetchAccounts();
        fetchSessions();
        setSearchUsername('');
      } else {
        const error = await response.json();
        alert(`Search failed: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error searching accounts:', error);
      alert('Failed to search accounts. Please try again.');
    } finally {
      setSearching(false);
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
                <h1 className="text-2xl font-bold text-gray-900">
                  Chimera
                </h1>
                <div className="flex items-center gap-4">
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
              <div className="space-y-6">
                {/* Greeting and Search */}
                <div className="flex items-center justify-between">
                  <h2 className="text-3xl font-bold text-gray-900">
                    Welcome back, {user?.firstName || user?.emailAddresses[0]?.emailAddress?.split('@')[0] || 'there'}!
                  </h2>
                  <button
                    onClick={() => setShowSearchForm(!showSearchForm)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Search Accounts
                  </button>
                </div>

                {/* Search Form */}
                {showSearchForm && (
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">Search for Your Accounts</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Enter a username to search across 300+ platforms and discover your accounts.
                    </p>
                    <div className="flex gap-3">
                      <input
                        type="text"
                        placeholder="Enter username..."
                        value={searchUsername}
                        onChange={(e) => setSearchUsername(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && searchAccounts()}
                        disabled={searching}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <button
                        onClick={searchAccounts}
                        disabled={searching || !searchUsername.trim()}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                      >
                        {searching ? (
                          <div className="flex items-center gap-2">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                            Searching...
                          </div>
                        ) : (
                          'Search'
                        )}
                      </button>
                      <button
                        onClick={() => {
                          setShowSearchForm(false);
                          setSearchResult(null);
                          setSearchUsername('');
                        }}
                        disabled={searching}
                        className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                    
                    {searchResult && (
                      <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-green-800 font-semibold">✓ Search completed!</p>
                        <p className="text-sm text-green-700 mt-1">
                          Found {searchResult.total_found} platforms, saved {searchResult.new_accounts_saved} new accounts.
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {/* Main Dashboard Layout */}
                <div className="grid grid-cols-12 gap-6">
                  {/* Left Sidebar - Buckets */}
                  <div className="col-span-3">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-900">Personas</h3>
                        <button
                          onClick={() => setShowNewBucketForm(!showNewBucketForm)}
                          className="text-blue-600 hover:text-blue-700 text-xl font-bold"
                          title="Add new bucket"
                        >
                          +
                        </button>
                      </div>
                      
                      {showNewBucketForm && (
                        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                          <input
                            type="text"
                            placeholder="Bucket name"
                            value={newBucketName}
                            onChange={(e) => setNewBucketName(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2 text-sm"
                          />
                          <input
                            type="text"
                            placeholder="Description (optional)"
                            value={newBucketDescription}
                            onChange={(e) => setNewBucketDescription(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2 text-sm"
                          />
                          <div className="flex gap-2">
                            <button
                              onClick={createBucket}
                              className="flex-1 px-3 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                            >
                              Create
                            </button>
                            <button
                              onClick={() => {
                                setShowNewBucketForm(false);
                                setNewBucketName('');
                                setNewBucketDescription('');
                              }}
                              className="flex-1 px-3 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm hover:bg-gray-300"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                      
                      <div className="space-y-2">
                        <button
                          onClick={() => setSelectedBucket(null)}
                          className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                            selectedBucket === null ? 'bg-gray-100' : 'hover:bg-gray-50'
                          }`}
                        >
                          <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
                          <span className="text-sm font-medium">All Accounts</span>
                        </button>
                        {buckets.map((bucket) => (
                          <div key={bucket.id} className="group relative">
                            <button
                              onClick={() => setSelectedBucket(bucket.id)}
                              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                selectedBucket === bucket.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                              }`}
                            >
                              <div className={`w-3 h-3 rounded-full ${
                                bucket.bucket_name === 'Personal' ? 'bg-black' :
                                bucket.bucket_name === 'Professional' ? 'bg-green-500' :
                                bucket.bucket_name === 'Development' ? 'bg-purple-500' :
                                'bg-red-500'
                              }`}></div>
                              <span className="text-sm font-medium flex-1 text-left">{bucket.bucket_name}</span>
                            </button>
                            <button
                              onClick={() => deleteBucket(bucket.id)}
                              className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 text-sm font-bold"
                              title="Delete bucket"
                            >
                              ×
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Main Content - Account Details */}
                  <div className="col-span-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h3 className="text-2xl font-bold text-gray-900 mb-6">
                        {selectedBucket ? buckets.find(b => b.id === selectedBucket)?.bucket_name : 'All Accounts'}
                      </h3>
                      
                      {accounts.filter(acc => !selectedBucket || acc.bucket?.id === selectedBucket).length === 0 ? (
                        <div className="text-center py-12">
                          <p className="text-gray-500">No accounts found</p>
                        </div>
                      ) : (
                        <div className="space-y-6">
                          {accounts.filter(acc => !selectedBucket || acc.bucket?.id === selectedBucket).map((account) => (
                            <div key={account.id} className="border-b border-gray-200 pb-4 last:border-0">
                              <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                  <h4 className="font-semibold text-gray-900">{account.platform}</h4>
                                  <p className="text-sm text-gray-600">{account.account_name}</p>
                                  {account.url && (
                                    <a 
                                      href={account.url} 
                                      target="_blank" 
                                      rel="noopener noreferrer"
                                      className="text-xs text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1 mt-1"
                                    >
                                      Visit profile
                                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                      </svg>
                                    </a>
                                  )}
                                </div>
                                <div className="flex items-center gap-2">
                                  {editingAccount === account.id ? (
                                    <select
                                      value={account.bucket?.id || ''}
                                      onChange={(e) => updateAccountBucket(account.id, e.target.value || null)}
                                      className="text-xs px-2 py-1 border border-gray-300 rounded"
                                    >
                                      <option value="">Unassigned</option>
                                      {buckets.map(bucket => (
                                        <option key={bucket.id} value={bucket.id}>
                                          {bucket.bucket_name}
                                        </option>
                                      ))}
                                    </select>
                                  ) : (
                                    <>
                                      <span 
                                        onClick={() => setEditingAccount(account.id)}
                                        className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded cursor-pointer hover:bg-gray-200"
                                      >
                                        {account.bucket?.name || 'Unassigned'}
                                      </span>
                                    </>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Right Sidebar - Statistics */}
                  <div className="col-span-3">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h3 className="text-lg font-bold text-gray-900 mb-4">Statistics</h3>
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-600">Total Accounts</p>
                          <p className="text-2xl font-bold text-gray-900">{accounts.length}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Total Buckets</p>
                          <p className="text-2xl font-bold text-gray-900">{buckets.length}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Unassigned Accounts</p>
                          <p className="text-2xl font-bold text-gray-900">
                            {accounts.filter(a => !a.bucket).length}
                          </p>
                        </div>
                      </div>
                    </div>
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







