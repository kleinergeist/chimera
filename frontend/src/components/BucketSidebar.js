import { useState } from 'react';

function BucketSidebar({ buckets, selectedBucket, onSelectBucket, onCreateBucket, onDeleteBucket }) {
  const [showNewBucketForm, setShowNewBucketForm] = useState(false);
  const [newBucketName, setNewBucketName] = useState('');
  const [newBucketDescription, setNewBucketDescription] = useState('');

  const handleCreateBucket = async () => {
    if (!newBucketName.trim()) return;
    
    const success = await onCreateBucket(newBucketName, newBucketDescription);
    if (success) {
      setShowNewBucketForm(false);
      setNewBucketName('');
      setNewBucketDescription('');
    }
  };

  const handleDeleteBucket = async (bucketId) => {
    if (!window.confirm('Are you sure you want to delete this bucket? Accounts will be unassigned.')) return;
    await onDeleteBucket(bucketId);
  };

  return (
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
              onClick={handleCreateBucket}
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
          onClick={() => onSelectBucket(null)}
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
              onClick={() => onSelectBucket(bucket.id)}
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
              onClick={() => handleDeleteBucket(bucket.id)}
              className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 text-sm font-bold"
              title="Delete bucket"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BucketSidebar;

