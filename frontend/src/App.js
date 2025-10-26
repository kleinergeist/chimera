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
  const [summary, setSummary] = useState(null);
  const [generatingSummary, setGeneratingSummary] = useState(false);
  const [splittingPersonas, setSplittingPersonas] = useState(false);
  const [personaResult, setPersonaResult] = useState(null);
  const [editingBucket, setEditingBucket] = useState(null);
  const [editBucketName, setEditBucketName] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [bucketToDelete, setBucketToDelete] = useState(null);

  useEffect(() => {
    if (user) {
      fetchUserData();
      fetchSessions();
      fetchBuckets();
      fetchAccounts();
    }
  }, [user]);

  // Clear summary and persona result when switching personas
  useEffect(() => {
    setSummary(null);
    setPersonaResult(null);
  }, [selectedBucket]);

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

  const updateBucket = async (bucketId, newName) => {
    if (!newName.trim()) return;
    
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/buckets/${bucketId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bucket_name: newName })
      });
      
      if (response.ok) {
        fetchBuckets();
        setEditingBucket(null);
        setEditBucketName('');
      } else {
        const error = await response.json();
        alert(`Failed to update bucket: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error updating bucket:', error);
      alert('Failed to update bucket. Please try again.');
    }
  };

  const confirmDeleteBucket = (bucketId) => {
    // Find the bucket to check if it's "Unassigned"
    const bucket = buckets.find(b => b.id === bucketId);
    if (bucket && bucket.bucket_name.toLowerCase().trim() === 'unassigned') {
      alert('Cannot delete the "Unassigned" bucket. This is a system bucket that must always exist.');
      return;
    }
    
    setBucketToDelete(bucketId);
    setShowDeleteModal(true);
  };

  const deleteBucket = async () => {
    if (!bucketToDelete) return;
    
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/buckets/${bucketToDelete}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        fetchBuckets();
        fetchAccounts();
        if (selectedBucket === bucketToDelete) {
          setSelectedBucket(null);
        }
        setShowDeleteModal(false);
        setBucketToDelete(null);
      } else {
        const error = await response.json();
        alert(`Failed to delete bucket: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error deleting bucket:', error);
      alert('Failed to delete bucket. Please try again.');
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

  const generateSummary = async () => {
    setGeneratingSummary(true);
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      // Prepare request body with persona filter
      const requestBody = {};
      if (selectedBucket) {
        requestBody.bucket_id = selectedBucket;
      }
      
      const response = await fetch(`${apiUrl}/api/generate-summary`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error('Error generating summary:', error);
    } finally {
      setGeneratingSummary(false);
    }
  };

  const splitPersonas = async () => {
    setSplittingPersonas(true);
    try {
      const token = await getToken();
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      // Prepare request body with persona filter
      const requestBody = {};
      if (selectedBucket) {
        requestBody.bucket_id = selectedBucket;
      }
      
      const response = await fetch(`${apiUrl}/api/split-personas`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      setPersonaResult(data);
      // Refresh buckets and accounts to show the new organization
      fetchBuckets();
      fetchAccounts();
    } catch (error) {
      console.error('Error splitting personas:', error);
      alert('Failed to split personas. Please try again.');
    } finally {
      setSplittingPersonas(false);
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
                            {editingBucket === bucket.id ? (
                              <div className="flex items-center gap-2 px-2 py-2 bg-blue-50 rounded-lg">
                                <input
                                  type="text"
                                  value={editBucketName}
                                  onChange={(e) => setEditBucketName(e.target.value)}
                                  onKeyPress={(e) => {
                                    if (e.key === 'Enter') {
                                      updateBucket(bucket.id, editBucketName);
                                    }
                                  }}
                                  className="flex-1 px-2 py-1 text-sm border border-blue-300 rounded"
                                  autoFocus
                                />
                                <button
                                  onClick={() => updateBucket(bucket.id, editBucketName)}
                                  className="text-green-600 hover:text-green-700 text-sm font-bold"
                                  title="Save"
                                >
                                  ✓
                                </button>
                                <button
                                  onClick={() => {
                                    setEditingBucket(null);
                                    setEditBucketName('');
                                  }}
                                  className="text-gray-500 hover:text-gray-700 text-sm font-bold"
                                  title="Cancel"
                                >
                                  ×
                                </button>
                              </div>
                            ) : (
                              <>
                                <button
                                  onClick={() => setSelectedBucket(bucket.id)}
                                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                    selectedBucket === bucket.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                                  }`}
                                >
                                  <span className="text-lg">
                                    {bucket.bucket_name.toLowerCase().includes('professional') || bucket.bucket_name.toLowerCase().includes('work') || bucket.bucket_name.toLowerCase().includes('career') ? '💼' :
                                     bucket.bucket_name.toLowerCase().includes('creative') || bucket.bucket_name.toLowerCase().includes('art') ? '🎨' :
                                     bucket.bucket_name.toLowerCase().includes('gaming') || bucket.bucket_name.toLowerCase().includes('game') ? '🎮' :
                                     bucket.bucket_name.toLowerCase().includes('development') || bucket.bucket_name.toLowerCase().includes('coding') ? '💻' :
                                     bucket.bucket_name.toLowerCase().includes('academic') || bucket.bucket_name.toLowerCase().includes('education') ? '📚' :
                                     bucket.bucket_name.toLowerCase().includes('financial') || bucket.bucket_name.toLowerCase().includes('finance') ? '💰' :
                                     bucket.bucket_name.toLowerCase().includes('personal') || bucket.bucket_name.toLowerCase().includes('social') ? '🏠' :
                                     bucket.bucket_name.toLowerCase().trim() === 'unassigned' ? '📂' :
                                     '📁'}
                                  </span>
                                  <span className="text-sm font-medium flex-1 text-left">
                                    {bucket.bucket_name}
                                    {bucket.bucket_name.toLowerCase().trim() === 'unassigned' && (
                                      <span className="ml-1 text-xs text-gray-500">(System)</span>
                                    )}
                                  </span>
                                </button>
                              </>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Main Content - Account Details */}
                  <div className="col-span-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between mb-6">
                        {editingBucket === selectedBucket ? (
                          <div className="flex items-center gap-3 flex-1">
                            <input
                              type="text"
                              value={editBucketName}
                              onChange={(e) => setEditBucketName(e.target.value)}
                              onKeyPress={(e) => {
                                if (e.key === 'Enter') {
                                  updateBucket(selectedBucket, editBucketName);
                                }
                              }}
                              className="text-2xl font-bold px-3 py-2 border border-blue-300 rounded-lg"
                              autoFocus
                            />
                            <button
                              onClick={() => updateBucket(selectedBucket, editBucketName)}
                              className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                            >
                              Save
                            </button>
                            <button
                              onClick={() => {
                                setEditingBucket(null);
                                setEditBucketName('');
                              }}
                              className="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-sm"
                            >
                              Cancel
                            </button>
                          </div>
                        ) : (
                          <>
                            <div className="flex items-center gap-3">
                              <h3 className="text-2xl font-bold text-gray-900">
                                {selectedBucket ? buckets.find(b => b.id === selectedBucket)?.bucket_name : 'All Accounts'}
                              </h3>
                              {selectedBucket && buckets.find(b => b.id === selectedBucket)?.bucket_name.toLowerCase().trim() !== 'unassigned' && (
                                <button
                                  onClick={() => {
                                    setEditingBucket(selectedBucket);
                                    const bucket = buckets.find(b => b.id === selectedBucket);
                                    setEditBucketName(bucket?.bucket_name || '');
                                  }}
                                  className="text-blue-500 hover:text-blue-700 text-sm font-bold"
                                  title="Edit persona name"
                                >
                                  ✎
                                </button>
                              )}
                            </div>
                            {selectedBucket && buckets.find(b => b.id === selectedBucket)?.bucket_name.toLowerCase().trim() !== 'unassigned' && (
                              <button
                                onClick={() => confirmDeleteBucket(selectedBucket)}
                                className="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
                              >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                                Delete Persona
                              </button>
                            )}
                          </>
                        )}
                      </div>
                      
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
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-900">Statistics</h3>
                        {selectedBucket && (
                          <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                            {buckets.find(b => b.id === selectedBucket)?.bucket_name}
                          </span>
                        )}
                      </div>
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-600">
                            {selectedBucket ? `${buckets.find(b => b.id === selectedBucket)?.bucket_name} Accounts` : 'Total Accounts'}
                          </p>
                          <p className="text-2xl font-bold text-gray-900">
                            {selectedBucket 
                              ? accounts.filter(a => a.bucket?.id === selectedBucket).length
                              : accounts.length
                            }
                          </p>
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
                        
                        {/* AI Summary Section */}
                        <div className="border-t border-gray-200 pt-4">
                          <div className="flex items-center justify-between mb-3">
                            <h4 className="text-sm font-semibold text-gray-700">AI Summary</h4>
                            <button
                              onClick={generateSummary}
                              disabled={generatingSummary || (selectedBucket ? accounts.filter(a => a.bucket?.id === selectedBucket).length === 0 : accounts.length === 0)}
                              className="px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
                            >
                              {generatingSummary ? (
                                <>
                                  <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                                  Generating...
                                </>
                              ) : (
                                'Generate Summary'
                              )}
                            </button>
                          </div>
                          
                          {summary ? (
                            <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-700 leading-relaxed">
                              <div 
                                className="markdown-content"
                                dangerouslySetInnerHTML={{
                                  __html: summary
                                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                    .replace(/^• (.+)$/gm, '<div class="ml-4">• $1</div>')
                                    .replace(/\n\n/g, '<br/><br/>')
                                    .replace(/\n/g, '<br/>')
                                }}
                              />
                              
                              {/* Split Personas Button */}
                              <div className="mt-3 pt-3 border-t border-gray-200">
                                <button
                                  onClick={splitPersonas}
                                  disabled={splittingPersonas || (selectedBucket ? accounts.filter(a => a.bucket?.id === selectedBucket).length === 0 : accounts.length === 0)}
                                  className="w-full px-3 py-2 text-xs bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                >
                                  {splittingPersonas ? (
                                    <>
                                      <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                                      Splitting Personas...
                                    </>
                                  ) : (
                                    <>
                                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                                      </svg>
                                      Split Personas
                                    </>
                                  )}
                                </button>
                                <p className="text-xs text-gray-500 mt-1 text-center">
                                  Organize accounts into separate personas to prevent identity leakage
                                </p>
                              </div>
                            </div>
                          ) : (
                            <div className="text-xs text-gray-500 italic">
                              {selectedBucket 
                                ? (accounts.filter(a => a.bucket?.id === selectedBucket).length === 0 
                                    ? `No accounts found in ${buckets.find(b => b.id === selectedBucket)?.bucket_name} persona.`
                                    : `Click 'Generate Summary' to get an AI analysis of your ${buckets.find(b => b.id === selectedBucket)?.bucket_name} persona based on discovered websites.`)
                                : (accounts.length === 0 
                                    ? "No accounts found. Search for accounts first to generate a summary."
                                    : "Click 'Generate Summary' to get an AI analysis of your digital presence based on discovered websites.")
                              }
                            </div>
                          )}
                          
                          {/* Persona Split Result */}
                          {personaResult && (
                            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                              <h5 className="text-sm font-semibold text-green-800 mb-2">Personas Created Successfully!</h5>
                              <div className="text-xs text-green-700 space-y-1">
                                <p>• {personaResult.buckets_created} persona buckets created</p>
                                <p>• {personaResult.accounts_assigned} accounts organized</p>
                                <div className="mt-2">
                                  <p className="font-medium">Personas:</p>
                                  {personaResult.personas?.map((persona, index) => (
                                    <div key={index} className="ml-2 text-xs">
                                      <span className="font-medium">{persona.name}:</span> {persona.platforms.join(', ')}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                          )}
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

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
            <div className="flex items-start gap-4 mb-4">
              <div className="flex-shrink-0 w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-gray-900 mb-2">Delete Persona</h3>
                <p className="text-sm text-gray-600 mb-1">
                  Are you sure you want to delete <span className="font-semibold">{buckets.find(b => b.id === bucketToDelete)?.bucket_name}</span>?
                </p>
                <p className="text-sm text-red-600 font-medium">
                  This action is irreversible. All accounts in this persona will be unassigned.
                </p>
              </div>
            </div>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => {
                  setShowDeleteModal(false);
                  setBucketToDelete(null);
                }}
                className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={deleteBucket}
                className="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
              >
                Delete Permanently
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;







