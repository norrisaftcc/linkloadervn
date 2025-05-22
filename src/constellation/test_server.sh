#!/bin/bash

# Constellation Engine Server Integration Test

echo "🧪 Testing Constellation Engine Server..."
echo ""

# Test configuration
BASE_URL="http://localhost:8083"
EXAMPLES_PATH="/examples"
UI_PATH="/ui"
CORE_PATH="/core"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASS=0
FAIL=0

# Test function
test_url() {
    local url="$1"
    local description="$2"
    local expected_status="${3:-200}"
    
    echo -n "Testing $description... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$response" -eq "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} ($response)"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC} ($response, expected $expected_status)"
        echo "   URL: $url"
        ((FAIL++))
    fi
}

# Test JSON validation
test_json() {
    local url="$1"
    local description="$2"
    
    echo -n "Testing $description JSON... "
    
    response=$(curl -s "$url")
    if echo "$response" | python -m json.tool > /dev/null 2>&1; then
        echo -e "${GREEN}✅ VALID JSON${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ INVALID JSON${NC}"
        echo "   URL: $url"
        echo "   Response: ${response:0:100}..."
        ((FAIL++))
    fi
}

echo "🌐 Basic Server Connectivity"
test_url "$BASE_URL" "Server root"

echo ""
echo "📁 Core Dependencies"
test_url "$BASE_URL$UI_PATH/constellation.css" "CSS file"
test_url "$BASE_URL$CORE_PATH/engine.js" "Engine JS"

echo ""
echo "📖 Main Pages"
test_url "$BASE_URL$EXAMPLES_PATH/index.html" "Story selection page"
test_url "$BASE_URL$EXAMPLES_PATH/player.html" "Universal player page"

echo ""
echo "📚 Story Files (JSON Validation)"
test_json "$BASE_URL$EXAMPLES_PATH/demo_story.json" "Demo story"
test_json "$BASE_URL$EXAMPLES_PATH/neon_taxidermy_intro.json" "Neon Taxidermy"
test_json "$BASE_URL$EXAMPLES_PATH/netrunner_heist.json" "Netrunner heist"

echo ""
echo "🎮 Player URLs with Story Parameters"
test_url "$BASE_URL$EXAMPLES_PATH/player.html?story=demo_story.json" "Demo story player"
test_url "$BASE_URL$EXAMPLES_PATH/player.html?story=neon_taxidermy_intro.json" "Neon Taxidermy player"

echo ""
echo "🔍 File Content Samples"
echo -n "CSS loads and contains 'constellation-engine'... "
if curl -s "$BASE_URL$UI_PATH/constellation.css" | grep -q "constellation-engine"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((FAIL++))
fi

echo -n "Engine JS contains 'ConstellationEngine'... "
if curl -s "$BASE_URL$CORE_PATH/engine.js" | grep -q "ConstellationEngine"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((FAIL++))
fi

echo -n "Neon Taxidermy contains 'First Light'... "
if curl -s "$BASE_URL$EXAMPLES_PATH/neon_taxidermy_intro.json" | grep -q "First Light"; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((FAIL++))
fi

echo ""
echo "📊 Test Results"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "✅ Passed: ${GREEN}$PASS${NC}"
echo -e "❌ Failed: ${RED}$FAIL${NC}"
echo -e "📈 Total:  $((PASS + FAIL))"

if [ $FAIL -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! Server is working correctly.${NC}"
    echo ""
    echo "🚀 Ready URLs:"
    echo "   Main Menu: $BASE_URL$EXAMPLES_PATH/index.html"
    echo "   Neon Taxidermy: $BASE_URL$EXAMPLES_PATH/player.html?story=neon_taxidermy_intro.json"
else
    echo ""
    echo -e "${RED}⚠️  Some tests failed. Check the issues above.${NC}"
    echo ""
    echo "💡 Common fixes:"
    echo "   - Make sure server is running from constellation/ directory"
    echo "   - Check file paths and permissions"
    echo "   - Verify JSON syntax in story files"
fi

echo ""