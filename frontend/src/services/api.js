// API service utilities for making authenticated requests

const getApiUrl = () => process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiService = {
  // User endpoints
  async fetchUserData(getToken) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Session endpoints
  async fetchSessions(getToken) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/sessions`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    return data.sessions || [];
  },

  // Bucket endpoints
  async fetchBuckets(getToken) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/buckets`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    return data.buckets || [];
  },

  async createBucket(getToken, bucketName, description) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/buckets`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        bucket_name: bucketName,
        description: description
      })
    });
    return response.ok;
  },

  async deleteBucket(getToken, bucketId) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/buckets/${bucketId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.ok;
  },

  // Account endpoints
  async fetchAccounts(getToken) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/accounts`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    return data.accounts || [];
  },

  async updateAccountBucket(getToken, accountId, bucketId) {
    const token = await getToken();
    const response = await fetch(`${getApiUrl()}/api/accounts/${accountId}/bucket`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ bucket_id: bucketId })
    });
    return response.ok;
  }
};

