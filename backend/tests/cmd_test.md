New Endpoints:
GET /users - Get all users from the database
POST /users - Create a new user
DELETE /users/{user_id} - Delete a user by ID
How to Test via Terminal:
1. Start Your Services:
2. View All Users:
> curl http://localhost:8000/users
3. Create a New User:
curl -X POST "http://localhost:8000/users?email=test@example.com&password=mypassword123"
4. Delete a User (replace 1 with actual user ID):
curl -X DELETE http://localhost:8000/users/1
5. Check Health:
 http://localhost:8000/health


# View all users with pretty formatting
curl -s http://localhost:8000/users | jq

# Create user and see formatted response
curl -s -X POST "http://localhost:8000/users?email=john@example.com&password=secret123" | jq