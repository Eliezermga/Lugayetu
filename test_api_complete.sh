#!/bin/bash

# Script de test complet de l'API Lugayetu
# Ce script teste tous les endpoints de l'API

BASE_URL="http://localhost:5000/api"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="testpass123"
ACCESS_TOKEN=""

echo "======================================"
echo "Test de l'API Lugayetu"
echo "======================================"
echo ""

# Fonction pour afficher les résultats
print_result() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
    else
        echo "❌ $2"
    fi
}

# 1. Test de l'endpoint GET /api/provinces (public)
echo "1. Test GET /api/provinces (endpoint public)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/provinces")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/provinces - SUCCESS"
    echo "Provinces disponibles: $(echo $BODY | jq -r '.data.provinces | length') provinces"
else
    echo "❌ GET /api/provinces - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 2. Test de l'inscription
echo "2. Test POST /api/register..."
REGISTER_DATA='{
  "nom": "Test",
  "prenom": "User",
  "age": 25,
  "sexe": "Homme",
  "langue_parlee": "Rund",
  "province": "Kinshasa",
  "ville_village": "Kinshasa",
  "email": "'$TEST_EMAIL'",
  "password": "'$TEST_PASSWORD'"
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d "$REGISTER_DATA")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ POST /api/register - SUCCESS"
    echo "Utilisateur créé: $(echo $BODY | jq -r '.data.email')"
else
    echo "❌ POST /api/register - FAILED (HTTP $HTTP_CODE)"
    echo "Réponse: $BODY"
fi
echo ""

# 3. Approuver l'utilisateur (nécessite l'accès admin)
echo "3. Approbation de l'utilisateur (via interface web)..."
echo "⚠️  L'utilisateur doit être approuvé par un admin avant de continuer"
echo "   Email admin: admin@lugayetu.cd"
echo "   Mot de passe admin: 31082003"
echo ""
read -p "Appuyez sur Entrée quand l'utilisateur est approuvé..."
echo ""

# 4. Test de connexion
echo "4. Test POST /api/login..."
LOGIN_DATA='{
  "email": "'$TEST_EMAIL'",
  "password": "'$TEST_PASSWORD'"
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "$LOGIN_DATA")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ POST /api/login - SUCCESS"
    ACCESS_TOKEN=$(echo $BODY | jq -r '.data.access_token')
    echo "Token obtenu: ${ACCESS_TOKEN:0:50}..."
else
    echo "❌ POST /api/login - FAILED (HTTP $HTTP_CODE)"
    echo "Réponse: $BODY"
    exit 1
fi
echo ""

# 5. Test GET /api/user/profile
echo "5. Test GET /api/user/profile..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/user/profile" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/user/profile - SUCCESS"
    echo "Profil: $(echo $BODY | jq -r '.data.prenom') $(echo $BODY | jq -r '.data.nom')"
else
    echo "❌ GET /api/user/profile - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 6. Test PUT /api/user/profile
echo "6. Test PUT /api/user/profile (modification du profil)..."
UPDATE_DATA='{
  "nom": "TestModifié",
  "age": 26
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/user/profile" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_DATA")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ PUT /api/user/profile - SUCCESS"
    echo "Nouveau nom: $(echo $BODY | jq -r '.data.nom')"
    echo "Nouvel âge: $(echo $BODY | jq -r '.data.age')"
else
    echo "❌ PUT /api/user/profile - FAILED (HTTP $HTTP_CODE)"
    echo "Réponse: $BODY"
fi
echo ""

# 7. Test GET /api/user/stats
echo "7. Test GET /api/user/stats..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/user/stats" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/user/stats - SUCCESS"
    echo "Enregistrements: $(echo $BODY | jq -r '.data.total_recordings')"
    echo "Durée totale: $(echo $BODY | jq -r '.data.total_duration_minutes') min"
else
    echo "❌ GET /api/user/stats - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 8. Test GET /api/languages
echo "8. Test GET /api/languages..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/languages" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/languages - SUCCESS"
    echo "Langues disponibles: $(echo $BODY | jq -r '.data.languages | length')"
else
    echo "❌ GET /api/languages - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 9. Test GET /api/sentences/next
echo "9. Test GET /api/sentences/next..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/sentences/next" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/sentences/next - SUCCESS"
    SENTENCE_ID=$(echo $BODY | jq -r '.data.sentence.id')
    echo "Prochaine phrase (ID: $SENTENCE_ID): $(echo $BODY | jq -r '.data.sentence.text')"
else
    echo "❌ GET /api/sentences/next - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 10. Test GET /api/recordings
echo "10. Test GET /api/recordings..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/recordings" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET /api/recordings - SUCCESS"
    echo "Nombre d'enregistrements: $(echo $BODY | jq -r '.data.pagination.total')"
else
    echo "❌ GET /api/recordings - FAILED (HTTP $HTTP_CODE)"
fi
echo ""

# 11. Test de suppression de compte (optionnel)
echo "11. Test DELETE /api/user/account (OPTIONNEL)..."
read -p "Voulez-vous tester la suppression de compte ? (o/N): " CONFIRM_DELETE

if [ "$CONFIRM_DELETE" = "o" ] || [ "$CONFIRM_DELETE" = "O" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/user/account" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)

    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ DELETE /api/user/account - SUCCESS"
        echo "Message: $(echo $BODY | jq -r '.message')"
    else
        echo "❌ DELETE /api/user/account - FAILED (HTTP $HTTP_CODE)"
    fi
else
    echo "⏭️  Test de suppression ignoré"
fi
echo ""

echo "======================================"
echo "Tests terminés!"
echo "======================================"
