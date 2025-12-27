"""Verify that the AI Governance Platform is properly installed."""
import sys

def check_imports():
    """Check that all required modules can be imported."""
    print("🔍 Checking imports...")
    
    required_modules = [
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("plotly", "Plotly"),
        ("numpy", "NumPy"),
    ]
    
    missing = []
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT FOUND")
            missing.append(name)
    
    return missing

def check_project_structure():
    """Check that all required files exist."""
    print("\n🔍 Checking project structure...")
    
    from pathlib import Path
    
    required_files = [
        "src/core/models.py",
        "src/gateway/llm_gateway.py",
        "src/detection/risk_engine.py",
        "src/policy/guardrails.py",
        "src/monitoring/cost_monitor.py",
        "src/audit/audit_logger.py",
        "src/platform/governance_platform.py",
        "app.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - NOT FOUND")
            missing.append(file_path)
    
    return missing

def check_platform():
    """Check that the platform can be initialized."""
    print("\n🔍 Checking platform initialization...")
    
    try:
        from src.platform.governance_platform import GovernancePlatform
        platform = GovernancePlatform()
        print("  ✅ Platform initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ Platform initialization failed: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("AI Governance Platform - Installation Verification")
    print("=" * 60)
    
    # Check imports
    missing_modules = check_imports()
    
    # Check structure
    missing_files = check_project_structure()
    
    # Check platform
    platform_ok = check_platform()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("\n✅ All required modules installed")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files present")
    
    if platform_ok:
        print("✅ Platform can be initialized")
    else:
        print("❌ Platform initialization failed")
    
    # Final verdict
    if not missing_modules and not missing_files and platform_ok:
        print("\n" + "=" * 60)
        print("🎉 Installation verified successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run test suite: python test_platform.py")
        print("  2. Start dashboard: streamlit run app.py")
        print("  3. Read QUICKSTART.md for usage guide")
        return 0
    else:
        print("\n" + "=" * 60)
        print("⚠️  Installation incomplete")
        print("=" * 60)
        print("\nPlease fix the issues above and run this script again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
