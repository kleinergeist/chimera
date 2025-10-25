import { useState, useEffect } from 'react';
import { useUser, useAuth } from '@clerk/clerk-react';
import Header from '../components/Header';
import BucketSidebar from '../components/BucketSidebar';
import AccountList from '../components/AccountList';
import StatisticsSidebar from '../components/StatisticsSidebar';
import { apiService } from '../services/api';

function Dashboard() {
  const { user } = useUser();
  const { getToken } = useAuth();
  const [userData, setUserData] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [buckets, setBuckets] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedBucket, setSelectedBucket] = useState(null);

  useEffect(() => {
    if (user) {
      fetchAllData();
    }
  }, [user]);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchUserData(),
        fetchSessions(),
        fetchBuckets(),
        fetchAccounts()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserData = async () => {
    try {
      const data = await apiService.fetchUserData(getToken);
      setUserData(data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchSessions = async () => {
    try {
      const data = await apiService.fetchSessions(getToken);
      setSessions(data);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchBuckets = async () => {
    try {
      const data = await apiService.fetchBuckets(getToken);
      setBuckets(data);
    } catch (error) {
      console.error('Error fetching buckets:', error);
    }
  };

  const fetchAccounts = async () => {
    try {
      const data = await apiService.fetchAccounts(getToken);
      setAccounts(data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const handleCreateBucket = async (bucketName, description) => {
    try {
      const success = await apiService.createBucket(getToken, bucketName, description);
      if (success) {
        await fetchBuckets();
      }
      return success;
    } catch (error) {
      console.error('Error creating bucket:', error);
      return false;
    }
  };

  const handleDeleteBucket = async (bucketId) => {
    try {
      const success = await apiService.deleteBucket(getToken, bucketId);
      if (success) {
        await fetchBuckets();
        await fetchAccounts();
        if (selectedBucket === bucketId) {
          setSelectedBucket(null);
        }
      }
      return success;
    } catch (error) {
      console.error('Error deleting bucket:', error);
      return false;
    }
  };

  const handleUpdateAccountBucket = async (accountId, bucketId) => {
    try {
      const success = await apiService.updateAccountBucket(getToken, accountId, bucketId);
      if (success) {
        await fetchAccounts();
      }
      return success;
    } catch (error) {
      console.error('Error updating account bucket:', error);
      return false;
    }
  };

  return (
    <div className="min-h-screen">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Greeting */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Welcome back, {user?.firstName || user?.emailAddresses[0]?.emailAddress?.split('@')[0] || 'there'}!
              </h2>
            </div>

            {/* Main Dashboard Layout */}
            <div className="grid grid-cols-12 gap-6">
              {/* Left Sidebar - Buckets */}
              <div className="col-span-3">
                <BucketSidebar
                  buckets={buckets}
                  selectedBucket={selectedBucket}
                  onSelectBucket={setSelectedBucket}
                  onCreateBucket={handleCreateBucket}
                  onDeleteBucket={handleDeleteBucket}
                />
              </div>

              {/* Main Content - Account Details */}
              <div className="col-span-6">
                <AccountList
                  accounts={accounts}
                  buckets={buckets}
                  selectedBucket={selectedBucket}
                  onUpdateAccountBucket={handleUpdateAccountBucket}
                />
              </div>

              {/* Right Sidebar - Statistics */}
              <div className="col-span-3">
                <StatisticsSidebar
                  accounts={accounts}
                  buckets={buckets}
                />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;

