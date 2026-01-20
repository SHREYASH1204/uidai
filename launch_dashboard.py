"""
Launch Script for Aadhaar DataThon Dashboard and PDF Generation
Hackathon-Winning Solution Launcher
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dashboard_requirements():
    """Install dashboard-specific requirements"""
    print("🔧 Installing dashboard requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "dashboard_requirements.txt"])
        print("✅ Dashboard requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dashboard requirements: {e}")
        return False

def generate_pdf_report():
    """Generate the hackathon-winning PDF report"""
    print("\n📄 Generating Hackathon-Winning PDF Report...")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, "pdf_report_generator.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ PDF Report generated successfully!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print("❌ PDF generation failed!")
            if result.stderr:
                print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ PDF generation timed out!")
        return False
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def launch_dashboard():
    """Launch the interactive Streamlit dashboard"""
    print("\n🚀 Launching Interactive Dashboard...")
    print("=" * 60)
    print("📊 Dashboard will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("=" * 60)
    
    try:
        # Launch Streamlit dashboard
        subprocess.run([sys.executable, "-m", "streamlit", "run", "interactive_dashboard.py", 
                       "--server.port", "8501", "--server.headless", "false"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def main():
    """Main launcher function"""
    print("🏆 AADHAAR DATATHON - HACKATHON WINNING SOLUTION")
    print("=" * 60)
    print("🎯 Interactive Dashboard + Professional PDF Report")
    print("🏛️ Digital India Analytics Platform")
    print("=" * 60)
    
    # Check if data files exist
    data_dirs = [
        "api_data_aadhar_biometric",
        "api_data_aadhar_demographic", 
        "api_data_aadhar_enrolment"
    ]
    
    missing_dirs = [d for d in data_dirs if not os.path.exists(d)]
    if missing_dirs:
        print(f"⚠️  Warning: Missing data directories: {missing_dirs}")
        print("📁 Please ensure all data directories are present")
    
    # Install requirements
    if not install_dashboard_requirements():
        print("❌ Failed to install requirements. Exiting.")
        return
    
    # Generate PDF report first
    pdf_success = generate_pdf_report()
    
    # Show options to user
    print("\n🎛️  LAUNCH OPTIONS:")
    print("1. 📊 Launch Interactive Dashboard")
    print("2. 📄 Generate PDF Report Only") 
    print("3. 🚀 Launch Both (Recommended)")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                launch_dashboard()
                break
            elif choice == "2":
                if not pdf_success:
                    generate_pdf_report()
                else:
                    print("✅ PDF report already generated!")
                break
            elif choice == "3":
                if not pdf_success:
                    generate_pdf_report()
                print("\n🎉 PDF Generated! Now launching dashboard...")
                input("Press Enter to continue to dashboard...")
                launch_dashboard()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏆 HACKATHON SUBMISSION SUMMARY")
    print("=" * 60)
    
    files_generated = []
    if os.path.exists("Aadhaar_DataThon_Winning_Report.pdf"):
        files_generated.append("📄 Aadhaar_DataThon_Winning_Report.pdf")
    
    if os.path.exists("interactive_dashboard.py"):
        files_generated.append("📊 Interactive Dashboard (interactive_dashboard.py)")
    
    if files_generated:
        print("✅ Generated Files:")
        for file in files_generated:
            print(f"   {file}")
    
    print("\n🎯 Submission Components:")
    print("   • Interactive Streamlit Dashboard with real-time analytics")
    print("   • Professional 8-page PDF report with comprehensive insights")
    print("   • Advanced machine learning analytics and predictions")
    print("   • Strategic recommendations for system optimization")
    print("   • Complete source code with documentation")
    
    print("\n🏛️ Ready for DataThon Submission!")

if __name__ == "__main__":
    main()