# Steps to run the backend server

## Set up a postgres db via docker
`docker run -p 5432:5432 -e POSTGRES_PASSWORD=your_password -d postgres`

## Create a .env file
In the root directory, create the `.env ` file and populate it. Use `env-sample` as a reference point.

## Start the backend server
Execute the `start_server.sh` file: `./start_server.sh`

### Available API endpoints:
- http://localhost:8000/api/transactions/
- http://localhost:8000/api/transactions/{id}
- http://localhost:8000/api/tax-liability/


