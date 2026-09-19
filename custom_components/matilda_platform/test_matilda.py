#!/usr/bin/env python3
"""
Test script for Matilda Platform integration.

Usage:
    python test_matilda.py
"""

import asyncio
import aiohttp
from pathlib import Path
import sys

# Add the integration to path
sys.path.insert(0, str(Path(__file__).parent))

from matilda_platform.api import MatildaPlatformAPI


async def main():
    """Test the API."""
    async with aiohttp.ClientSession() as session:
        api = MatildaPlatformAPI(session)

        print("=" * 60)
        print("Testing Matilda Platform API")
        print("=" * 60)

        # Test 1: Fetch distributors
        print("\n1. Fetching distributors...")
        distributors = await api.get_distributors()
        print(f"   Found {len(distributors)} distributors")

        if distributors:
            # Show a few examples
            print("\n   Examples:")
            for dist in distributors[:5]:
                print(
                    f"   - {dist['name']} (ID: {dist['id']}, "
                    f"City: {dist.get('address', {}).get('addressLocality', 'N/A')})"
                )

            # Test 2: Fetch menu for first distributor
            print("\n2. Fetching menu for first distributor...")
            first_dist = distributors[0]
            print(f"   School: {first_dist['name']}")
            print(f"   ID: {first_dist['id']}")

            menu_data = await api.get_menu(first_dist["id"])

            if menu_data:
                print(f"   API Response: {len(str(menu_data))} bytes")
                parsed = api.parse_menu(menu_data)
                print(f"\n   Parsed menu:\n{parsed}")
            else:
                print("   No menu data returned")

            # Test 3: Test some schools
            print("\n3. Testing some schools...")
            test_schools = [
                distributors[0],
                distributors[1] if len(distributors) > 1 else distributors[0],
            ]

            for school in test_schools:
                print(f"\n   {school['name']}:")
                menu_data = await api.get_menu(school["id"])
                parsed = api.parse_menu(menu_data)
                lines = parsed.split("\n")[:3]
                print("   " + "\n   ".join(lines))
                if len(parsed.split("\n")) > 3:
                    print("   ...")

        print("\n" + "=" * 60)
        print("Test completed!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
