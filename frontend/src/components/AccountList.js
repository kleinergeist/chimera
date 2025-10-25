import { useState } from 'react';

function AccountList({ accounts, buckets, selectedBucket, onUpdateAccountBucket }) {
  const [editingAccount, setEditingAccount] = useState(null);

  const filteredAccounts = accounts.filter(acc => 
    !selectedBucket || acc.bucket?.id === selectedBucket
  );

  const selectedBucketName = selectedBucket 
    ? buckets.find(b => b.id === selectedBucket)?.bucket_name 
    : 'All Accounts';

  const handleUpdateBucket = async (accountId, bucketId) => {
    const success = await onUpdateAccountBucket(accountId, bucketId || null);
    if (success) {
      setEditingAccount(null);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">
        {selectedBucketName}
      </h3>
      
      {filteredAccounts.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No accounts found</p>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredAccounts.map((account) => (
            <div key={account.id} className="border-b border-gray-200 pb-4 last:border-0">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">{account.platform}</h4>
                  <p className="text-sm text-gray-600">{account.account_name}</p>
                </div>
                <div className="flex items-center gap-2">
                  {editingAccount === account.id ? (
                    <select
                      value={account.bucket?.id || ''}
                      onChange={(e) => handleUpdateBucket(account.id, e.target.value)}
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
                    <span 
                      onClick={() => setEditingAccount(account.id)}
                      className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded cursor-pointer hover:bg-gray-200"
                    >
                      {account.bucket?.name || 'Unassigned'}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AccountList;

