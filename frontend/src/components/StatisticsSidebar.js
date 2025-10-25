function StatisticsSidebar({ accounts, buckets }) {
  const unassignedCount = accounts.filter(a => !a.bucket).length;

  return (
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
          <p className="text-2xl font-bold text-gray-900">{unassignedCount}</p>
        </div>
      </div>
    </div>
  );
}

export default StatisticsSidebar;

