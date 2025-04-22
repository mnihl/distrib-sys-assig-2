# Distributed Systems Assignment 2.
Assignment 2: Service Oriented Architectures Web Services and REST

By: Eniko Balint, Daniel Csorba, Morgan Nihlmar

## 1. Authentication Service

The team decided on using Flask for the project since it is a great lightweight solution for REST APIs. In the Authentication service logic can be found for signing up and token verification. It runs on port 5000, which is the default for Flask. Since the service had to be implemented without an in-memory storage we used hard-coded users. The users had the following attributes: name, password and role. 

The login POST method checks if the given user credentials are correct and uses the create_token function (which has a basic token creation logic based on the requirements) to emit a token. The token contains the user's role, since with the implemented authorization funcionality not every role can access every function.

And lastly, in the verify function we verify the token.


## 2. Transaction Service

### Overview

We went with Flask for our transaction service because it is easy to set up, supports RESTful design patterns, and is more than sufficient for the functionality required of this assignment.

The service stores transaction metadata and fraud prediction results separately.It runs on localhost with port 5001. 
- Users are able to:
    - Add transactions via POST method /transaction
    - Update transactions via PUT method /transaction/<int: transaction_id>
    - View fraud detection results (some test data has been injected in results as it is not performed by the functionality of the service currently, accessed with ID = 1) via GET method /result/<int: transaction_id>
Authorization is enforced via tokens that contain user roles. Only users with the role `agent` or `administrator` can interact with the service.

### Database Tables

This service persists data in a local `SQLite` database (`transactions.db`) with two tables:

1. **transactions**
   - `id`, `customer`, `timestamp`, `status`, `vendor_id`, `amount`

2. **results**
   - `id`, `transaction_id`, `timestamp`, `is_fraudulent`, `confidence`


### Logging
Every incoming request is logged to stdout with the following metadata:
- Source IP
- URL
- Headers
- Body
- Timestamp

### 3. Testing the services (use Postman)

1. Start the flask apps in separate terminals
**In /authentication_service/**
```bash
python authen.py
```
**In /transaction_service/**
```bash
python app.py
```

2. Login authentication
- Method: POST
- URL: http://localhost:5000/login
- Body: (Test with any of the users in users_db variable of authen.py if desired)
```json
{
    "username": "admin1",
    "password": "password1"
}
```
You will now receive the assigned token

3. Verify token
- Method: POST
- URL: http://localhost:5000/verify
- Body:
```json (Use the one received from previous step)
{
    "token": "Administrator:fGVDVUHuu1"
}
```
Should receive "Token is valid"

4. Add a transaction
- Method: POST
- URL: http://localhost:5001/transaction
- Headers: 
    - Content-Type: application/json
    - Authorization: Administrator:fGVDVUHuu1
- Body:
```json
{
  "customer": "Alice Smith",
  "timestamp": "2025-04-20T14:00:00",
  "status": "submitted",
  "vendor_id": "VENDOR456",
  "amount": 349.50
}
```

5. Update an Existing Transaction
- Method: PUT
- URL: http://localhost:5001/transaction/1
- Headers:
    - Content-Type: application/json
    - Authorization: Administrator:fGVDVUHuu1
- Body:
```json
{
  "status": "accepted",
  "vendor_id": "VENDOR456",
  "amount": 349.50
}
```

6. Fetch Prediction Results
- Method: GET
- URL: http://localhost:5001/result/1
- Headers:
- Authorization: Administrator:fGVDVUHuu1
