#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

EMAIL="john@example.com"
PASSWORD="mypassword"

echo "----- CREATE USER -----"

CREATE_USER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
-H "Content-Type: application/json" \
-d "{
\"first_name\":\"John\",
\"last_name\":\"Doe\",
\"email\":\"$EMAIL\",
\"password\":\"$PASSWORD\"
}")

echo $CREATE_USER_RESPONSE
echo ""

echo "----- LOGIN -----"

LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
-H "Content-Type: application/json" \
-d "{
\"email\":\"$EMAIL\",
\"password\":\"$PASSWORD\"
}")

echo $LOGIN_RESPONSE

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token',''))")

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed"
    exit 1
fi

echo "✅ Token obtained"
echo ""

echo "----- CREATE PLACE -----"

CREATE_PLACE_RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"title": "Test Place",
"description": "Test description",
"price": 100,
"latitude": 48.85,
"longitude": 2.35,
"amenities": []
}')

echo $CREATE_PLACE_RESPONSE

PLACE_ID=$(echo $CREATE_PLACE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id',''))")

if [ -z "$PLACE_ID" ]; then
    echo "❌ Place creation failed"
    exit 1
fi

echo "✅ Place created: $PLACE_ID"
echo ""

echo "----- GET PLACES (PUBLIC ENDPOINT) -----"

curl -s -X GET $BASE_URL/places/
echo ""
echo ""

echo "----- CREATE REVIEW -----"

CREATE_REVIEW_RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d "{
\"text\": \"Great place\",
\"rating\": 5,
\"place_id\": \"$PLACE_ID\"
}")

echo $CREATE_REVIEW_RESPONSE

REVIEW_ID=$(echo $CREATE_REVIEW_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id',''))")

echo "Review ID: $REVIEW_ID"
echo ""

echo "----- UPDATE REVIEW -----"

curl -s -X PUT $BASE_URL/reviews/$REVIEW_ID \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"text": "Updated review",
"rating": 4
}'
echo ""
echo ""

echo "----- DELETE REVIEW -----"

curl -s -X DELETE $BASE_URL/reviews/$REVIEW_ID \
-H "Authorization: Bearer $TOKEN"

echo ""
echo ""
echo "----- TEST COMPLETE -----"
