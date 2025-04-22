# Distributed Systems Assignment 2.
Assignment 2: Service Oriented Architectures Web Services and REST

By: Eniko Balint, Daniel Csorba, Morgan Nihlmar

# 1. Authentication service: 
this service will be responsible for authenticating and logging users into the
system. The following user groups (roles) are defined:
###
* Administrator: can create and delete users and manage all types of data.
* Secretary: can access only the customer data.
* Agent: can receive fraud notification alerts, monitor and re-train the ML fraud detection system.

The service will expose an authentication API with the following functions:
###
* A function that accepts username/password and, if correct, emits a simple token (containing user
role and a random base-64 string).
* A function for verifying that the token for a given user is still valid.
This service will be implemented with an in-memory cache (without persistent storage).
# 2. Transaction service: 
this service will be responsible for storing the metadata for the customers’ transactions and manage at least two data tables in a persistent data store:
###
* transactions: a table containing metadata information for each customer transaction (customer,
timestamp, status (submitted, accepted, rejected), vendor-ID, amount).
* results: a table containing metadata information for the predictions of the ML system for each
transaction (transaction ID, timestamp, is-fraudulent, confidence).

The service will expose an API for importing new transactions, updating them and fetching the prediction
results for each transaction. Note that only users of the user group agents and administrators are allowed
to use this service. All other users and unauthenticated users will get an authorization error.
# Deadline: 2025/04/22, 23:59 CET.

Remarks
###
* You are free to use any programming language of your choice. You can even use different programming
languages for different services, if you deem this appropriate.
* All files shall be submitted in a single zip file.
* A README.MD file will also be included in the submission with a short description of the sumitted files.
* You may build a simple web UI for testing - since UI development is out of the scope of the course, it
will not be graded.
* Every request performed by a client and all server responses must be logged with the following information: source, destination, headers (if applicable), metadata (if applicable), message body.
* You have free choice as to what web service/communication framework to use for each service: please
explain your choice in the README.MD file.
* Don’t spend much time on the business logic: please focus on setting up the services, APIs between
services and logging.


Assessment
Total: 15 points.
###
* All requirements are satisfied: 10 points.
* The documentation is concise and the choice on which web service/framework was used is well explained
and technically correct: 5 points

## 1. Authentication Service




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

1. Start the flask apps in separate termins
* In /authentication-service/
```bash
python authen.py
```
* In /transaction-service/
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
    - Authorization: agent-token
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
    - Authorization: agent-token
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
- Authorization: agent-token