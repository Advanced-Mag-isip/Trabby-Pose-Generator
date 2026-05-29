#!/usr/bin/env python
"""
Trabby Pose Backend - Setup Verification Script

Run this script to verify that all models, serializers, and endpoints are working correctly.

Usage:
    python test_setup.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from api.models import PuppetPart, PosePreset, PartConfiguration
from api.serializers import (
    PuppetPartSerializer,
    PosePresetListSerializer,
    PosePresetDetailSerializer,
    PartConfigurationSerializer
)
from django.test import Client
from django.urls import reverse
import json


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def test_models():
    """Test that models are correctly defined."""
    print_header("Testing Models")
    
    # Test PuppetPart count
    part_count = PuppetPart.objects.count()
    if part_count > 0:
        print_success(f"Found {part_count} puppet parts")
    else:
        print_error("No puppet parts found. Run 'python manage.py seed_assets'")
        return False
    
    # Test PosePreset count
    pose_count = PosePreset.objects.count()
    if pose_count > 0:
        print_success(f"Found {pose_count} pose presets")
    else:
        print_error("No pose presets found. Run 'python manage.py seed_assets'")
        return False
    
    # Test PartConfiguration count
    config_count = PartConfiguration.objects.count()
    if config_count > 0:
        print_success(f"Found {config_count} part configurations")
    else:
        print_error("No part configurations found. Run 'python manage.py seed_assets'")
        return False
    
    # Test specific pose
    try:
        neutral_pose = PosePreset.objects.get(slug='neutral')
        print_success(f"Found 'neutral' pose with {neutral_pose.part_configurations.count()} parts")
    except PosePreset.DoesNotExist:
        print_error("'neutral' pose not found")
        return False
    
    # Test body poses vs expressions
    body_poses = PosePreset.objects.filter(is_expression=False)
    expressions = PosePreset.objects.filter(is_expression=True)
    print_success(f"Body poses: {body_poses.count()}, Expressions: {expressions.count()}")
    
    return True


def test_serializers():
    """Test that serializers work correctly."""
    print_header("Testing Serializers")
    
    try:
        # Test PuppetPartSerializer
        part = PuppetPart.objects.first()
        if part:
            serializer = PuppetPartSerializer(part)
            data = serializer.data
            assert 'name' in data
            assert 'asset_url' in data
            assert 'part_type' in data
            print_success("PuppetPartSerializer working")
        
        # Test PosePresetListSerializer
        pose = PosePreset.objects.filter(is_expression=False).first()
        if pose:
            serializer = PosePresetListSerializer(pose)
            data = serializer.data
            assert 'name' in data
            assert 'slug' in data
            assert 'part_count' in data
            print_success("PosePresetListSerializer working")
        
        # Test PosePresetDetailSerializer
        if pose:
            serializer = PosePresetDetailSerializer(pose)
            data = serializer.data
            assert 'name' in data
            assert 'part_configurations' in data
            assert len(data['part_configurations']) > 0
            assert 'puppet_part' in data['part_configurations'][0]
            print_success("PosePresetDetailSerializer working with nested data")
        
        return True
    
    except Exception as e:
        print_error(f"Serializer test failed: {str(e)}")
        return False


def test_api_endpoints():
    """Test API endpoints."""
    print_header("Testing API Endpoints")
    
    client = Client()
    
    # Test /api/poses/
    try:
        response = client.get('/api/poses/')
        if response.status_code == 200:
            data = response.json()
            if 'count' in data and 'data' in data:
                print_success(f"GET /api/poses/ returned {data['count']} poses")
            else:
                print_error("Unexpected response format from /api/poses/")
                return False
        else:
            print_error(f"GET /api/poses/ returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"GET /api/poses/ failed: {str(e)}")
        return False
    
    # Test /api/poses/<slug>/
    try:
        response = client.get('/api/poses/neutral/')
        if response.status_code == 200:
            data = response.json()
            if 'slug' in data and 'part_configurations' in data:
                print_success(f"GET /api/poses/neutral/ returned detailed config with {len(data['part_configurations'])} parts")
            else:
                print_error("Unexpected response format from /api/poses/neutral/")
                return False
        else:
            print_error(f"GET /api/poses/neutral/ returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"GET /api/poses/neutral/ failed: {str(e)}")
        return False
    
    # Test /api/expressions/
    try:
        response = client.get('/api/expressions/')
        if response.status_code == 200:
            data = response.json()
            if 'count' in data and 'data' in data:
                print_success(f"GET /api/expressions/ returned {data['count']} expressions")
            else:
                print_error("Unexpected response format from /api/expressions/")
                return False
        else:
            print_error(f"GET /api/expressions/ returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"GET /api/expressions/ failed: {str(e)}")
        return False
    
    # Test /api/puppet-parts/
    try:
        response = client.get('/api/puppet-parts/')
        if response.status_code == 200:
            data = response.json()
            if 'count' in data and 'data' in data:
                print_success(f"GET /api/puppet-parts/ returned {data['count']} parts")
            else:
                print_error("Unexpected response format from /api/puppet-parts/")
                return False
        else:
            print_error(f"GET /api/puppet-parts/ returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"GET /api/puppet-parts/ failed: {str(e)}")
        return False
    
    # Test /api/puppet-parts/ with filter
    try:
        response = client.get('/api/puppet-parts/?part_type=HEAD')
        if response.status_code == 200:
            data = response.json()
            if 'count' in data:
                print_success(f"GET /api/puppet-parts/?part_type=HEAD returned {data['count']} head parts")
            else:
                print_error("Filter failed")
                return False
        else:
            print_error(f"Filter request returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Filter request failed: {str(e)}")
        return False
    
    # Test /api/test/
    try:
        response = client.get('/api/test/')
        if response.status_code == 200:
            data = response.json()
            if 'message' in data:
                print_success(f"GET /api/test/ working: {data['message']}")
            else:
                print_error("Unexpected response format from /api/test/")
                return False
        else:
            print_error(f"GET /api/test/ returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"GET /api/test/ failed: {str(e)}")
        return False
    
    return True


def test_data_integrity():
    """Test data integrity."""
    print_header("Testing Data Integrity")
    
    try:
        # Verify poses have parts
        for pose in PosePreset.objects.all():
            part_count = pose.part_configurations.count()
            if part_count == 0:
                print_error(f"Pose '{pose.name}' has no parts")
                return False
        
        print_success("All poses have at least one part")
        
        # Verify all referenced parts exist
        for config in PartConfiguration.objects.all():
            if config.puppet_part is None:
                print_error(f"PartConfiguration has null puppet_part")
                return False
        
        print_success("All part configurations reference valid parts")
        
        # Verify z-index ordering
        for pose in PosePreset.objects.all():
            configs = pose.part_configurations.all()
            z_indices = [c.z_index for c in configs]
            if len(z_indices) != len(set(z_indices)):
                print_error(f"Pose '{pose.name}' has duplicate z-indices")
                return False
        
        print_success("All z-indices are unique within each pose")
        
        return True
    
    except Exception as e:
        print_error(f"Data integrity check failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  🧪 Trabby Pose Backend - Setup Verification")
    print("="*60)
    
    results = []
    
    results.append(("Models", test_models()))
    results.append(("Serializers", test_serializers()))
    results.append(("API Endpoints", test_api_endpoints()))
    results.append(("Data Integrity", test_data_integrity()))
    
    print_header("Summary")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n" + "="*60)
        print("  🎉 All Tests Passed! Backend is Ready!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Start server: python manage.py runserver")
        print("  2. Visit: http://localhost:8000/api/poses/")
        print("  3. Connect frontend to the API")
        print("\nDocumentation:")
        print("  - README.md: Project overview")
        print("  - API_DOCUMENTATION.md: Full API reference")
        print("  - SETUP_GUIDE.md: Detailed setup")
        print("  - QUICK_REFERENCE.md: Quick commands")
        return 0
    else:
        print("\n" + "="*60)
        print("  ❌ Some Tests Failed!")
        print("="*60)
        print("\nTroubleshooting:")
        print("  1. Make sure you ran migrations: python manage.py migrate")
        print("  2. Make sure you seeded data: python manage.py seed_assets")
        print("  3. Check environment variables in .env")
        print("  4. Review SETUP_GUIDE.md for detailed instructions")
        return 1


if __name__ == '__main__':
    sys.exit(main())
