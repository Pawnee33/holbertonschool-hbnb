#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

ADMIN_EMAIL="admin@hbnb.io"
ADMIN_PASSWORD="admin1234"

USER_EMAIL="john@example.com"
USER_PASSWORD="mypassword"

USER2_EMAIL="jane@example.com"
USER2_PASSWORD="mypassword2"

# ----- LOGIN ADMIN -----
echo "----- LOGIN ADMIN -----"
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
-H "Content-Type: application/json" \
-d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}")
echo $ADMIN_LOGIN

ADMIN_TOKEN=$(echo $ADMIN_LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

if [ -z "$ADMIN_TOKEN" ]; then
    echo "❌ Admin login failed — did you run: flask shell + db.create_all() + load schema.sql ?"
    exit 1
fi
echo "✅ Admin token obtained"
echo ""

# ----- CREATE USER 1 (via admin) -----
echo "----- CREATE USER 1 -----"
CREATE_USER=$(curl -s -X POST $BASE_URL/users/ \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d "{\"first_name\":\"John\",\"last_name\":\"Doe\",\"email\":\"$USER_EMAIL\",\"password\":\"$USER_PASSWORD\"}")
echo $CREATE_USER
echo ""

# ----- CREATE USER 2 (via admin) -----
echo "----- CREATE USER 2 -----"
CREATE_USER2=$(curl -s -X POST $BASE_URL/users/ \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d "{\"first_name\":\"Jane\",\"last_name\":\"Doe\",\"email\":\"$USER2_EMAIL\",\"password\":\"$USER2_PASSWORD\"}")
echo $CREATE_USER2
echo ""

# ----- LOGIN USER 1 -----
echo "----- LOGIN USER 1 -----"
LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
-H "Content-Type: application/json" \
-d "{\"email\":\"$USER_EMAIL\",\"password\":\"$USER_PASSWORD\"}")
echo $LOGIN
TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$TOKEN" ]; then echo "❌ Login failed"; exit 1; fi
echo "✅ User1 token obtained"
echo ""

# ----- LOGIN USER 2 -----
echo "----- LOGIN USER 2 -----"
LOGIN2=$(curl -s -X POST $BASE_URL/auth/login \
-H "Content-Type: application/json" \
-d "{\"email\":\"$USER2_EMAIL\",\"password\":\"$USER2_PASSWORD\"}")
echo $LOGIN2
TOKEN2=$(echo $LOGIN2 | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$TOKEN2" ]; then echo "❌ Login2 failed"; exit 1; fi
echo "✅ User2 token obtained"
echo ""

# ----- CREATE PLACE (user1) -----
echo "----- CREATE PLACE -----"
CREATE_PLACE=$(curl -s -X POST $BASE_URL/places/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Test Place","description":"Test description","price":100,"latitude":48.85,"longitude":2.35,"amenities":[]}')
echo $CREATE_PLACE
PLACE_ID=$(echo $CREATE_PLACE | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
if [ -z "$PLACE_ID" ]; then echo "❌ Place creation failed"; exit 1; fi
echo "✅ Place created: $PLACE_ID"
echo ""

# ----- GET PLACES (public) -----
echo "----- GET PLACES (PUBLIC) -----"
curl -s -X GET $BASE_URL/places/
echo ""
echo ""

# ----- CREATE REVIEW (user2 reviews user1's place) -----
echo "----- CREATE REVIEW -----"
CREATE_REVIEW=$(curl -s -X POST $BASE_URL/reviews/ \
-H "Authorization: Bearer $TOKEN2" \
-H "Content-Type: application/json" \
-d "{\"text\":\"Great place\",\"rating\":5,\"place_id\":\"$PLACE_ID\"}")
echo $CREATE_REVIEW
REVIEW_ID=$(echo $CREATE_REVIEW | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
if [ -z "$REVIEW_ID" ]; then echo "❌ Review creation failed"; exit 1; fi
echo "✅ Review created: $REVIEW_ID"
echo ""

# ----- UPDATE REVIEW (user2) -----
echo "----- UPDATE REVIEW -----"
curl -s -X PUT $BASE_URL/reviews/$REVIEW_ID \
-H "Authorization: Bearer $TOKEN2" \
-H "Content-Type: application/json" \
-d '{"text":"Updated review","rating":4}'
echo ""
echo ""

# ----- DELETE REVIEW (user2) -----
echo "----- DELETE REVIEW -----"
curl -s -X DELETE $BASE_URL/reviews/$REVIEW_ID \
-H "Authorization: Bearer $TOKEN2"
echo ""
echo ""

echo "----- TEST COMPLETE ✅ -----"
