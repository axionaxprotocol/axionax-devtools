#!/bin/bash
#
# AxionAx Testnet Readiness Checker - Bash Wrapper
# Comprehensive pre-launch validation for AxionAx Protocol testnet deployment
#
# Usage:
#   ./check-testnet-readiness.sh
#   ./check-testnet-readiness.sh --verbose
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Parse arguments
VERBOSE=0
if [[ "$1" == "--verbose" || "$1" == "-v" ]]; then
    VERBOSE=1
fi

# Banner
echo ""
echo -e "${CYAN}======================================================================${NC}"
echo -e "${BOLD}${CYAN}  AXIONAX TESTNET READINESS CHECKER${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# Check Python installation
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}  ❌ Python not found. Please install Python 3.8+.${NC}"
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}  ✅ Python: $PYTHON_VERSION${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Locate checker script
CHECKER_SCRIPT="$SCRIPT_DIR/axionax-devtools/scripts/testing/testnet_readiness_checker.py"

if [ ! -f "$CHECKER_SCRIPT" ]; then
    echo -e "${RED}  ❌ Readiness checker script not found at: $CHECKER_SCRIPT${NC}"
    exit 1
fi

echo -e "${GREEN}  ✅ Checker script found${NC}"
echo ""

# Run the checker
echo -e "${YELLOW}Running comprehensive testnet readiness checks...${NC}"
echo ""

cd "$SCRIPT_DIR"

EXIT_CODE=0
if [ $VERBOSE -eq 1 ]; then
    $PYTHON_CMD "$CHECKER_SCRIPT" -v || EXIT_CODE=$?
else
    $PYTHON_CMD "$CHECKER_SCRIPT" || EXIT_CODE=$?
fi

# Check for report
REPORT_PATH="$SCRIPT_DIR/TESTNET_READINESS_REPORT.json"

if [ -f "$REPORT_PATH" ]; then
    echo ""
    echo -e "${CYAN}Detailed JSON report generated: TESTNET_READINESS_REPORT.json${NC}"
    
    # Parse and display key metrics (requires jq for pretty parsing, but optional)
    if command -v jq &> /dev/null; then
        echo ""
        echo -e "${CYAN}======================================================================${NC}"
        echo -e "${BOLD}${CYAN}  KEY METRICS${NC}"
        echo -e "${CYAN}======================================================================${NC}"
        echo ""
        
        OVERALL_PASSED=$(jq -r '.overall_passed' "$REPORT_PATH")
        OVERALL_SCORE=$(jq -r '.overall_score' "$REPORT_PATH")
        
        if [ "$OVERALL_PASSED" == "true" ]; then
            echo -e "${GREEN}  Overall Status: ✅ READY${NC}"
        else
            echo -e "${RED}  Overall Status: ❌ NOT READY${NC}"
        fi
        
        echo -e "${YELLOW}  Overall Score:  $OVERALL_SCORE/100${NC}"
        echo ""
        
        # Count critical issues
        CRITICAL_COUNT=$(jq '[.results[] | select(.critical == true and .passed == false)] | length' "$REPORT_PATH")
        
        if [ "$CRITICAL_COUNT" -gt 0 ]; then
            echo -e "${RED}  🚨 CRITICAL ISSUES (Must Fix): $CRITICAL_COUNT${NC}"
            jq -r '.results[] | select(.critical == true and .passed == false) | "    • \(.name): \(.message)"' "$REPORT_PATH"
            echo ""
        fi
        
        echo -e "${CYAN}======================================================================${NC}"
        echo ""
    fi
fi

# Final recommendations
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}${BOLD}🎉 TESTNET LAUNCH APPROVED!${NC}"
    echo -e "${GREEN}   System passed all critical checks and is ready for deployment.${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "  1. Schedule deployment window"
    echo -e "  2. Notify validators and community"
    echo -e "  3. Prepare rollback procedures"
    echo -e "  4. Monitor system health during launch"
else
    echo -e "${RED}${BOLD}⚠️  TESTNET NOT READY${NC}"
    echo -e "${YELLOW}   Please address the issues above before proceeding with launch.${NC}"
    echo ""
    echo -e "${YELLOW}Recommended Actions:${NC}"
    echo -e "  1. Fix all critical security issues"
    echo -e "  2. Complete missing documentation"
    echo -e "  3. Run security audit"
    echo -e "  4. Re-run this checker after fixes"
fi

echo ""

exit $EXIT_CODE
