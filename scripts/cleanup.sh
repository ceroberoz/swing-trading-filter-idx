#!/bin/bash
# Cleanup and maintenance script for Swing Trading Filter (IDX)
# This script helps manage output files, logs, and cache

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Swing Trading Filter - Cleanup Utility${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}\n"

# Function to print section headers
print_section() {
    echo -e "\n${YELLOW}▶ $1${NC}"
}

# Function to confirm action
confirm() {
    read -p "$(echo -e ${YELLOW}$1 [y/N]: ${NC})" -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# Navigate to project directory
cd "$PROJECT_DIR"

# Main menu
show_menu() {
    echo -e "${GREEN}Select cleanup option:${NC}"
    echo "  1) Clean old scan results (>30 days)"
    echo "  2) Clean old backtest results (>30 days)"
    echo "  3) Clean old charts (>30 days)"
    echo "  4) Clean all old output files (>30 days)"
    echo "  5) Clean logs (>30 days)"
    echo "  6) Clean cache (yfinance cache)"
    echo "  7) Clean all (output + logs + cache)"
    echo "  8) Archive important results"
    echo "  9) Show disk usage"
    echo "  0) Exit"
    echo
}

# Clean old scans
clean_scans() {
    print_section "Cleaning old scan results (>30 days)..."

    if [ -d "output/scans" ]; then
        COUNT=$(find output/scans/ -name "*.txt" -mtime +30 2>/dev/null | wc -l)
        if [ "$COUNT" -gt 0 ]; then
            echo "Found $COUNT files to delete"
            if confirm "Delete $COUNT old scan files?"; then
                find output/scans/ -name "*.txt" -mtime +30 -delete
                echo -e "${GREEN}✓ Deleted $COUNT scan files${NC}"
            else
                echo -e "${YELLOW}Skipped${NC}"
            fi
        else
            echo -e "${GREEN}No old scan files found${NC}"
        fi
    else
        echo -e "${YELLOW}output/scans/ directory not found${NC}"
    fi
}

# Clean old backtests
clean_backtests() {
    print_section "Cleaning old backtest results (>30 days)..."

    if [ -d "output/backtests" ]; then
        COUNT=$(find output/backtests/ -name "*.txt" -o -name "*.json" -o -name "*.csv" | xargs -I {} find {} -mtime +30 2>/dev/null | wc -l)
        if [ "$COUNT" -gt 0 ]; then
            echo "Found $COUNT files to delete"
            if confirm "Delete $COUNT old backtest files?"; then
                find output/backtests/ \( -name "*.txt" -o -name "*.json" -o -name "*.csv" \) -mtime +30 -delete
                echo -e "${GREEN}✓ Deleted $COUNT backtest files${NC}"
            else
                echo -e "${YELLOW}Skipped${NC}"
            fi
        else
            echo -e "${GREEN}No old backtest files found${NC}"
        fi
    else
        echo -e "${YELLOW}output/backtests/ directory not found${NC}"
    fi
}

# Clean old charts
clean_charts() {
    print_section "Cleaning old charts (>30 days)..."

    if [ -d "output/charts" ]; then
        COUNT=$(find output/charts/ -name "*.png" -o -name "*.jpg" | xargs -I {} find {} -mtime +30 2>/dev/null | wc -l)
        if [ "$COUNT" -gt 0 ]; then
            echo "Found $COUNT files to delete"
            if confirm "Delete $COUNT old chart files?"; then
                find output/charts/ \( -name "*.png" -o -name "*.jpg" \) -mtime +30 -delete
                echo -e "${GREEN}✓ Deleted $COUNT chart files${NC}"
            else
                echo -e "${YELLOW}Skipped${NC}"
            fi
        else
            echo -e "${GREEN}No old chart files found${NC}"
        fi
    else
        echo -e "${YELLOW}output/charts/ directory not found${NC}"
    fi
}

# Clean logs
clean_logs() {
    print_section "Cleaning old logs (>30 days)..."

    if [ -d "logs" ]; then
        COUNT=$(find logs/ -name "*.log" -mtime +30 2>/dev/null | wc -l)
        if [ "$COUNT" -gt 0 ]; then
            echo "Found $COUNT log files to delete"
            if confirm "Delete $COUNT old log files?"; then
                find logs/ -name "*.log" -mtime +30 -delete
                echo -e "${GREEN}✓ Deleted $COUNT log files${NC}"
            else
                echo -e "${YELLOW}Skipped${NC}"
            fi
        else
            echo -e "${GREEN}No old log files found${NC}"
        fi
    else
        echo -e "${YELLOW}logs/ directory not found${NC}"
    fi
}

# Clean cache
clean_cache() {
    print_section "Cleaning yfinance cache..."

    if [ -d "cache" ]; then
        SIZE=$(du -sh cache/ 2>/dev/null | cut -f1)
        echo "Current cache size: $SIZE"
        if confirm "Delete cache? (Will be regenerated on next run)"; then
            rm -rf cache/*.db* 2>/dev/null || true
            echo -e "${GREEN}✓ Cache cleaned${NC}"
        else
            echo -e "${YELLOW}Skipped${NC}"
        fi
    else
        echo -e "${YELLOW}cache/ directory not found${NC}"
    fi
}

# Archive important results
archive_results() {
    print_section "Archiving important results..."

    CURRENT_QUARTER=$(date +%Y)Q$(( ($(date +%-m)-1)/3 + 1 ))
    ARCHIVE_DIR="output/archive/$CURRENT_QUARTER"

    echo "Archive directory: $ARCHIVE_DIR"

    if confirm "Archive backtest summaries to $ARCHIVE_DIR?"; then
        mkdir -p "$ARCHIVE_DIR"

        # Copy backtest summaries (files with "summary" in name)
        if [ -d "output/backtests" ]; then
            COUNT=$(find output/backtests/ -name "*summary*" 2>/dev/null | wc -l)
            if [ "$COUNT" -gt 0 ]; then
                cp output/backtests/*summary* "$ARCHIVE_DIR/" 2>/dev/null || true
                echo -e "${GREEN}✓ Archived $COUNT summary files${NC}"
            else
                echo -e "${YELLOW}No summary files found${NC}"
            fi
        fi

        # Copy important charts
        if [ -d "output/charts" ]; then
            COUNT=$(find output/charts/ -name "*performance*.png" 2>/dev/null | wc -l)
            if [ "$COUNT" -gt 0 ]; then
                cp output/charts/*performance*.png "$ARCHIVE_DIR/" 2>/dev/null || true
                echo -e "${GREEN}✓ Archived $COUNT performance charts${NC}"
            else
                echo -e "${YELLOW}No performance charts found${NC}"
            fi
        fi

        echo -e "${GREEN}✓ Archive complete: $ARCHIVE_DIR${NC}"
    else
        echo -e "${YELLOW}Skipped${NC}"
    fi
}

# Show disk usage
show_disk_usage() {
    print_section "Disk Usage Report"

    echo -e "\n${GREEN}Directory sizes:${NC}"
    [ -d "output" ] && echo "  output/     $(du -sh output/ 2>/dev/null | cut -f1)"
    [ -d "logs" ] && echo "  logs/       $(du -sh logs/ 2>/dev/null | cut -f1)"
    [ -d "cache" ] && echo "  cache/      $(du -sh cache/ 2>/dev/null | cut -f1)"

    echo -e "\n${GREEN}Output breakdown:${NC}"
    [ -d "output/scans" ] && echo "  scans/      $(du -sh output/scans/ 2>/dev/null | cut -f1) ($(find output/scans/ -name "*.txt" 2>/dev/null | wc -l) files)"
    [ -d "output/backtests" ] && echo "  backtests/  $(du -sh output/backtests/ 2>/dev/null | cut -f1) ($(find output/backtests/ -type f 2>/dev/null | wc -l) files)"
    [ -d "output/charts" ] && echo "  charts/     $(du -sh output/charts/ 2>/dev/null | cut -f1) ($(find output/charts/ -name "*.png" 2>/dev/null | wc -l) files)"

    echo -e "\n${GREEN}File counts by age:${NC}"
    if [ -d "output" ]; then
        LAST_7=$(find output/ -type f -mtime -7 2>/dev/null | wc -l)
        LAST_30=$(find output/ -type f -mtime -30 2>/dev/null | wc -l)
        OLDER_30=$(find output/ -type f -mtime +30 2>/dev/null | wc -l)
        echo "  Last 7 days:  $LAST_7 files"
        echo "  Last 30 days: $LAST_30 files"
        echo "  Older than 30 days: $OLDER_30 files"
    fi
}

# Main loop
while true; do
    show_menu
    read -p "Enter option: " choice

    case $choice in
        1) clean_scans ;;
        2) clean_backtests ;;
        3) clean_charts ;;
        4)
            clean_scans
            clean_backtests
            clean_charts
            ;;
        5) clean_logs ;;
        6) clean_cache ;;
        7)
            clean_scans
            clean_backtests
            clean_charts
            clean_logs
            clean_cache
            ;;
        8) archive_results ;;
        9) show_disk_usage ;;
        0)
            echo -e "\n${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac

    echo -e "\n${BLUE}════════════════════════════════════════════════${NC}"
done
