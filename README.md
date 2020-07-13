
Develop solutions in Python according to the following specifications taking consideration for security best practice, commenting, logging and exception handling.

REST Web Service
Develop a REST web service that:

1. Takes an embedded CSV file and stores its contents in a SQLite database without writing to disk.
2. Takes a range of time and returns all CSV data that was submitted (not created) within a given time frame.
3. Searches records for the given parameters and values, supporting all database fields.
4. Takes the same CSV data in JSON format and validates that each field contains the correct data types (e.g. a string field contains a string, a integer field contains a integer).
5. Allows records to be marked as "read" and "unread".
6. Returns an authentication token upon being provided with the following credentials:
     Username: superman
     Password: Th!sIsW£ak
7. Restricts all functionality to authenticated requests.
8. Implements TLS using a self-signed certificate.

REST Client CLI tool
Develop a corresponding client CLI tool that:

1. Authenticates with the web service.
2. Submits a CSV file to the REST web service.
3. Facilitates the utilisation of functionality described in numbers 2 and 3.
4. Facilitates polling of records at a configurable interval of seconds, using the functionality described in number 3 listed above. Polling should continue until interrupted.
5. Takes a CSV file in the format provided and converts it to JSON before submitting it via the functionality described in number 4.
6. Marks a given record as "read" or "unread".
