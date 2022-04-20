#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"

export AUTH0_DOMAIN="dev-9z1pdcyd.us.auth0.com"
export AUTH0_CLIENT_ID="wzZ2pQmzRJKFTn8PtXuvxGu8UhMzdF52"
export AUTH0_ALGORITHMS="RS256"
export AUTH0_API_AUDIENCE="casting_agency"

export DOMAIN="localhost"
export PORT="8080"
export PROTOCOL="http"
export HOST="$PROTOCOL://$DOMAIN:$PORT"
echo "setup.sh script executed successfully!"