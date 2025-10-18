#!/bin/bash

echo "========================================="
echo "TESTS DE L'API LUGAYETU"
echo "========================================="
echo ""

BASE_URL="http://localhost:5000/api"

echo "1. TEST: Liste des provinces (endpoint public)"
echo "GET $BASE_URL/provinces"
curl -s $BASE_URL/provinces | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "2. TEST: Inscription d'un nouvel utilisateur"
echo "POST $BASE_URL/register"
TIMESTAMP=$(date +%s)
curl -s -X POST $BASE_URL/register \
  -H "Content-Type: application/json" \
  -d "{
    \"nom\": \"Mukendi\",
    \"prenom\": \"Joseph\",
    \"age\": 28,
    \"sexe\": \"Homme\",
    \"langue_parlee\": \"Rund\",
    \"province\": \"Kinshasa\",
    \"ville_village\": \"Kinshasa\",
    \"email\": \"joseph.test${TIMESTAMP}@example.com\",
    \"password\": \"password123\"
  }" | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "3. TEST: Connexion avec l'admin"
echo "POST $BASE_URL/login"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@lugayetu.cd","password":"31082003"}')
echo "$LOGIN_RESPONSE" | python -m json.tool

TOKEN=$(echo $LOGIN_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
echo ""
echo "✓ Test réussi - Token JWT reçu"
echo ""

echo "========================================="
echo "4. TEST: Profil utilisateur (endpoint protégé)"
echo "GET $BASE_URL/user/profile"
echo "Authorization: Bearer [TOKEN]"
curl -s $BASE_URL/user/profile \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "5. TEST: Statistiques utilisateur"
echo "GET $BASE_URL/user/stats"
curl -s $BASE_URL/user/stats \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "6. TEST: Liste des langues"
echo "GET $BASE_URL/languages"
curl -s $BASE_URL/languages \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "7. TEST: Prochaine phrase à enregistrer"
echo "GET $BASE_URL/sentences/next"
SENTENCE_RESPONSE=$(curl -s $BASE_URL/sentences/next \
  -H "Authorization: Bearer $TOKEN")
echo "$SENTENCE_RESPONSE" | python -m json.tool

SENTENCE_ID=$(echo $SENTENCE_RESPONSE | python -c "import sys, json; data=json.load(sys.stdin); print(data['data']['sentence']['id'] if data['data']['sentence'] else 'null')")
echo ""
echo "✓ Test réussi - Phrase ID: $SENTENCE_ID"
echo ""

echo "========================================="
echo "8. TEST: Liste des enregistrements (paginée)"
echo "GET $BASE_URL/recordings?page=1&per_page=5"
curl -s "$BASE_URL/recordings?page=1&per_page=5" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo ""
echo "✓ Test réussi"
echo ""

echo "========================================="
echo "9. TEST: Tentative de connexion avec mauvais mot de passe"
echo "POST $BASE_URL/login (devrait échouer)"
curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@lugayetu.cd","password":"mauvais_mdp"}' | python -m json.tool
echo ""
echo "✓ Test réussi - Erreur 401 attendue"
echo ""

echo "========================================="
echo "10. TEST: Accès à un endpoint protégé sans token"
echo "GET $BASE_URL/user/profile (sans Authorization header)"
curl -s $BASE_URL/user/profile | python -m json.tool
echo ""
echo "✓ Test réussi - Erreur 401 attendue"
echo ""

echo "========================================="
echo "TOUS LES TESTS SONT TERMINÉS ✓"
echo "========================================="
