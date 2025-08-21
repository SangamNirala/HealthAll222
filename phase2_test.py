#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class Phase2PatientManagementTester:
    def __init__(self, base_url="https://followup-testing.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:300]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

            self.test_results.append({
                'name': name,
                'success': success,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response': response.text[:500] if not success else "OK"
            })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })
            return False, {}

    def test_phase2_patient_management_apis(self):
        """Test Phase 2 Patient Management System API endpoints as requested in review"""
        print("\n🏥 Testing Phase 2 Patient Management System APIs...")
        print("🎯 FOCUS: AdvancedAdherenceMonitor, AutomatedReportGenerator, IntelligentAlertSystem")
        
        # Test IDs as specified in review request
        provider_id = "provider-123"
        patient_id = "patient-456"
        
        print(f"📋 Test Parameters: Provider ID: {provider_id}, Patient ID: {patient_id}")
        
        # Test AdvancedAdherenceMonitor APIs (3 endpoints)
        adherence_success = self.test_advanced_adherence_monitor_apis(provider_id, patient_id)
        
        # Test AutomatedReportGenerator APIs (2 endpoints)
        report_success = self.test_automated_report_generator_apis(provider_id, patient_id)
        
        # Test IntelligentAlertSystem APIs (4 endpoints)
        alert_success = self.test_intelligent_alert_system_apis(provider_id, patient_id)
        
        print(f"\n📊 Phase 2 Patient Management System Test Summary:")
        print(f"   ✅ AdvancedAdherenceMonitor APIs: {'PASS' if adherence_success else 'FAIL'}")
        print(f"   ✅ AutomatedReportGenerator APIs: {'PASS' if report_success else 'FAIL'}")
        print(f"   ✅ IntelligentAlertSystem APIs: {'PASS' if alert_success else 'FAIL'}")
        
        overall_success = adherence_success and report_success and alert_success
        print(f"   🎯 Overall Phase 2 Success: {'✅ PASS' if overall_success else '❌ FAIL'}")
        
        return overall_success

    def test_advanced_adherence_monitor_apis(self, provider_id, patient_id):
        """Test AdvancedAdherenceMonitor APIs (3 endpoints)"""
        print("\n📊 Testing AdvancedAdherenceMonitor APIs...")
        
        # Test 1: POST /api/provider/patient-management/adherence - Create adherence monitoring
        adherence_data = {
            "patient_id": patient_id,
            "provider_id": provider_id,
            "adherence_type": "MEDICATION",
            "target_item": "Metformin 500mg",
            "tracking_period": "weekly",
            "expected_frequency": 14,  # twice daily for 7 days
            "next_review_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        
        success1, adherence_response = self.run_test(
            "Create Adherence Monitoring",
            "POST",
            "provider/patient-management/adherence",
            200,
            data=adherence_data
        )
        
        # Validate adherence monitoring response structure
        adherence_id = None
        if success1 and adherence_response:
            expected_keys = ['id', 'patient_id', 'provider_id', 'adherence_type', 'target_item', 'adherence_percentage', 'adherence_status']
            missing_keys = [key for key in expected_keys if key not in adherence_response]
            if not missing_keys:
                print(f"   ✅ Adherence monitoring response contains required keys")
                adherence_id = adherence_response.get('id')
                print(f"   📋 Created adherence monitoring ID: {adherence_id}")
                print(f"   📊 Adherence percentage: {adherence_response.get('adherence_percentage', 0)}%")
                print(f"   📈 Adherence status: {adherence_response.get('adherence_status', 'N/A')}")
                
                # Check for AI insights
                ai_insights = adherence_response.get('ai_insights', [])
                if ai_insights:
                    print(f"   🤖 AI insights provided: {len(ai_insights)} insights")
                    print(f"   💡 Sample insight: {ai_insights[0] if ai_insights else 'None'}")
                
                # Check for predictive risk score
                risk_score = adherence_response.get('predictive_risk_score', 0)
                print(f"   ⚠️ Predictive risk score: {risk_score}")
            else:
                print(f"   ❌ Adherence monitoring response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: GET /api/provider/patient-management/adherence/{patient_id} - Get adherence data with AI insights
        success2, adherence_get_response = self.run_test(
            "Get Adherence Data with AI Insights",
            "GET",
            f"provider/patient-management/adherence/{patient_id}",
            200
        )
        
        # Validate adherence data response
        if success2 and adherence_get_response:
            expected_keys = ['patient_id', 'adherence_records', 'ai_insights', 'risk_assessment']
            missing_keys = [key for key in expected_keys if key not in adherence_get_response]
            if not missing_keys:
                print(f"   ✅ Adherence data response contains required keys")
                
                # Validate adherence records
                records = adherence_get_response.get('adherence_records', [])
                print(f"   📊 Found {len(records)} adherence records")
                
                if records:
                    record = records[0]
                    record_keys = ['id', 'adherence_type', 'target_item', 'adherence_percentage', 'adherence_status']
                    missing_record_keys = [key for key in record_keys if key not in record]
                    if not missing_record_keys:
                        print(f"   ✅ Adherence record structure valid")
                        print(f"   💊 Target item: {record.get('target_item', 'N/A')}")
                        print(f"   📈 Adherence: {record.get('adherence_percentage', 0)}% ({record.get('adherence_status', 'N/A')})")
                    else:
                        print(f"   ❌ Adherence record missing keys: {missing_record_keys}")
                
                # Validate AI insights
                ai_insights = adherence_get_response.get('ai_insights', [])
                print(f"   🤖 AI insights: {len(ai_insights)} insights provided")
                
                # Validate risk assessment
                risk_assessment = adherence_get_response.get('risk_assessment', {})
                if risk_assessment:
                    print(f"   ⚠️ Risk assessment provided with {len(risk_assessment)} factors")
            else:
                print(f"   ❌ Adherence data response missing keys: {missing_keys}")
                success2 = False
        
        # Test 3: PUT /api/provider/patient-management/adherence/{adherence_id} - Update adherence data
        if adherence_id:
            update_data = {
                "adherence_percentage": 85.5,
                "adherence_status": "GOOD",
                "actual_frequency": 12,
                "missed_instances": 2,
                "perfect_days": 5,
                "improvement_trend": 5.2,
                "barriers_identified": ["forgetfulness", "side_effects"],
                "intervention_strategies": ["reminder_app", "dose_timing_adjustment"]
            }
            
            success3, update_response = self.run_test(
                "Update Adherence Data",
                "PUT",
                f"provider/patient-management/adherence/{adherence_id}",
                200,
                data=update_data
            )
            
            # Validate update response
            if success3 and update_response:
                expected_keys = ['id', 'adherence_percentage', 'adherence_status', 'improvement_trend']
                missing_keys = [key for key in expected_keys if key not in update_response]
                if not missing_keys:
                    print(f"   ✅ Adherence update response contains required keys")
                    print(f"   📊 Updated adherence: {update_response.get('adherence_percentage', 0)}%")
                    print(f"   📈 Status: {update_response.get('adherence_status', 'N/A')}")
                    print(f"   📊 Improvement trend: {update_response.get('improvement_trend', 0)}%")
                    
                    # Check for barriers and interventions
                    barriers = update_response.get('barriers_identified', [])
                    interventions = update_response.get('intervention_strategies', [])
                    print(f"   🚧 Barriers identified: {len(barriers)} barriers")
                    print(f"   🎯 Intervention strategies: {len(interventions)} strategies")
                else:
                    print(f"   ❌ Adherence update response missing keys: {missing_keys}")
                    success3 = False
        else:
            print("   ⚠️ Skipping adherence update test - no adherence ID available")
            success3 = True  # Don't fail the test if we couldn't get an ID
        
        return success1 and success2 and success3

    def test_automated_report_generator_apis(self, provider_id, patient_id):
        """Test AutomatedReportGenerator APIs (2 endpoints)"""
        print("\n📄 Testing AutomatedReportGenerator APIs...")
        
        # Test 1: POST /api/provider/patient-management/reports - Generate automated report with AI
        report_data = {
            "report_type": "PATIENT_SUMMARY",
            "report_format": "PDF",
            "title": f"Patient Summary Report - {patient_id}",
            "patient_id": patient_id,
            "provider_id": provider_id,
            "report_period": "monthly",
            "data_range": {
                "start_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
                "end_date": datetime.utcnow().isoformat()
            },
            "charts_included": ["adherence_trends", "progress_metrics", "ai_insights"],
            "scheduled_generation": False
        }
        
        success1, report_response = self.run_test(
            "Generate Automated Report with AI",
            "POST",
            "provider/patient-management/reports",
            200,
            data=report_data
        )
        
        # Validate report generation response
        report_id = None
        if success1 and report_response:
            expected_keys = ['id', 'report_type', 'title', 'provider_id', 'generation_status', 'ai_insights_included']
            missing_keys = [key for key in expected_keys if key not in report_response]
            if not missing_keys:
                print(f"   ✅ Report generation response contains required keys")
                report_id = report_response.get('id')
                print(f"   📄 Generated report ID: {report_id}")
                print(f"   📊 Report type: {report_response.get('report_type', 'N/A')}")
                print(f"   📈 Generation status: {report_response.get('generation_status', 'N/A')}")
                print(f"   🤖 AI insights included: {report_response.get('ai_insights_included', False)}")
                
                # Check for generated data
                generated_data = report_response.get('generated_data', {})
                if generated_data:
                    print(f"   📊 Generated data sections: {len(generated_data)} sections")
                    
                    # Check for AI insights in generated data
                    ai_insights = generated_data.get('ai_insights', [])
                    if ai_insights:
                        print(f"   🤖 AI insights in report: {len(ai_insights)} insights")
                        print(f"   💡 Sample AI insight: {ai_insights[0] if ai_insights else 'None'}")
                
                # Check for charts
                charts = report_response.get('charts_included', [])
                print(f"   📊 Charts included: {len(charts)} charts - {charts}")
                
                # Check file information
                file_path = report_response.get('file_path')
                file_size = report_response.get('file_size')
                if file_path:
                    print(f"   📁 File path: {file_path}")
                if file_size:
                    print(f"   📏 File size: {file_size} bytes")
            else:
                print(f"   ❌ Report generation response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: GET /api/provider/patient-management/reports/{provider_id} - Get provider reports
        success2, reports_response = self.run_test(
            "Get Provider Reports",
            "GET",
            f"provider/patient-management/reports/{provider_id}",
            200
        )
        
        # Validate provider reports response
        if success2 and reports_response:
            expected_keys = ['provider_id', 'reports', 'total_reports', 'recent_reports']
            missing_keys = [key for key in expected_keys if key not in reports_response]
            if not missing_keys:
                print(f"   ✅ Provider reports response contains required keys")
                
                # Validate reports list
                reports = reports_response.get('reports', [])
                total_reports = reports_response.get('total_reports', 0)
                print(f"   📄 Total reports: {total_reports}")
                print(f"   📊 Reports in response: {len(reports)}")
                
                if reports:
                    report = reports[0]
                    report_keys = ['id', 'report_type', 'title', 'generation_status', 'generated_at']
                    missing_report_keys = [key for key in report_keys if key not in report]
                    if not missing_report_keys:
                        print(f"   ✅ Report object structure valid")
                        print(f"   📄 Sample report: {report.get('title', 'N/A')}")
                        print(f"   📊 Type: {report.get('report_type', 'N/A')}")
                        print(f"   📈 Status: {report.get('generation_status', 'N/A')}")
                        
                        # Check for AI insights flag
                        ai_included = report.get('ai_insights_included', False)
                        print(f"   🤖 AI insights included: {ai_included}")
                    else:
                        print(f"   ❌ Report object missing keys: {missing_report_keys}")
                
                # Validate recent reports
                recent_reports = reports_response.get('recent_reports', [])
                print(f"   📅 Recent reports: {len(recent_reports)} reports")
            else:
                print(f"   ❌ Provider reports response missing keys: {missing_keys}")
                success2 = False
        
        return success1 and success2

    def test_intelligent_alert_system_apis(self, provider_id, patient_id):
        """Test IntelligentAlertSystem APIs (4 endpoints)"""
        print("\n🚨 Testing IntelligentAlertSystem APIs...")
        
        # Test 1: POST /api/provider/patient-management/alerts - Create smart alert
        alert_data = {
            "patient_id": patient_id,
            "provider_id": provider_id,
            "category": "ADHERENCE",
            "severity": "WARNING",
            "title": "Medication Adherence Decline",
            "message": "Patient adherence has dropped below 80% for Metformin",
            "detailed_description": "Patient has missed 3 doses in the past week, showing a declining adherence pattern",
            "data_source": "adherence_monitoring",
            "triggering_values": {
                "adherence_percentage": 75.5,
                "missed_doses": 3,
                "threshold": 80.0
            },
            "recommended_actions": [
                "Contact patient to discuss barriers",
                "Review medication timing",
                "Consider reminder system"
            ]
        }
        
        success1, alert_response = self.run_test(
            "Create Smart Alert",
            "POST",
            "provider/patient-management/alerts",
            200,
            data=alert_data
        )
        
        # Validate smart alert response
        alert_id = None
        if success1 and alert_response:
            expected_keys = ['id', 'patient_id', 'provider_id', 'category', 'severity', 'title', 'urgency_score', 'ai_confidence']
            missing_keys = [key for key in expected_keys if key not in alert_response]
            if not missing_keys:
                print(f"   ✅ Smart alert response contains required keys")
                alert_id = alert_response.get('id')
                print(f"   🚨 Created alert ID: {alert_id}")
                print(f"   📊 Category: {alert_response.get('category', 'N/A')}")
                print(f"   ⚠️ Severity: {alert_response.get('severity', 'N/A')}")
                print(f"   📈 Urgency score: {alert_response.get('urgency_score', 0)}")
                print(f"   🤖 AI confidence: {alert_response.get('ai_confidence', 0)}")
                
                # Check for recommended actions
                actions = alert_response.get('recommended_actions', [])
                print(f"   🎯 Recommended actions: {len(actions)} actions")
                
                # Check for escalation path
                escalation = alert_response.get('escalation_path', [])
                if escalation:
                    print(f"   📈 Escalation path: {len(escalation)} steps")
                
                # Check for similar cases
                similar_cases = alert_response.get('similar_cases', [])
                if similar_cases:
                    print(f"   🔍 Similar cases: {len(similar_cases)} cases found")
            else:
                print(f"   ❌ Smart alert response missing keys: {missing_keys}")
                success1 = False
        
        # Test 2: GET /api/provider/patient-management/alerts/{provider_id} - Get provider alerts
        success2, alerts_response = self.run_test(
            "Get Provider Alerts",
            "GET",
            f"provider/patient-management/alerts/{provider_id}",
            200
        )
        
        # Validate provider alerts response
        if success2 and alerts_response:
            expected_keys = ['provider_id', 'active_alerts', 'alert_summary', 'priority_alerts']
            missing_keys = [key for key in expected_keys if key not in alerts_response]
            if not missing_keys:
                print(f"   ✅ Provider alerts response contains required keys")
                
                # Validate active alerts
                active_alerts = alerts_response.get('active_alerts', [])
                print(f"   🚨 Active alerts: {len(active_alerts)} alerts")
                
                if active_alerts:
                    alert = active_alerts[0]
                    alert_keys = ['id', 'category', 'severity', 'title', 'urgency_score', 'status']
                    missing_alert_keys = [key for key in alert_keys if key not in alert]
                    if not missing_alert_keys:
                        print(f"   ✅ Alert object structure valid")
                        print(f"   🚨 Sample alert: {alert.get('title', 'N/A')}")
                        print(f"   ⚠️ Severity: {alert.get('severity', 'N/A')}")
                        print(f"   📊 Status: {alert.get('status', 'N/A')}")
                    else:
                        print(f"   ❌ Alert object missing keys: {missing_alert_keys}")
                
                # Validate alert summary
                alert_summary = alerts_response.get('alert_summary', {})
                if alert_summary:
                    print(f"   📊 Alert summary provided with {len(alert_summary)} metrics")
                    
                    # Check for severity breakdown
                    if 'severity_breakdown' in alert_summary:
                        severity_breakdown = alert_summary['severity_breakdown']
                        print(f"   ⚠️ Severity breakdown: {severity_breakdown}")
                
                # Validate priority alerts
                priority_alerts = alerts_response.get('priority_alerts', [])
                print(f"   🔥 Priority alerts: {len(priority_alerts)} high-priority alerts")
            else:
                print(f"   ❌ Provider alerts response missing keys: {missing_keys}")
                success2 = False
        
        # Test 3: POST /api/provider/patient-management/alert-rules - Create alert rules
        rule_data = {
            "provider_id": provider_id,
            "rule_name": "Medication Adherence Threshold",
            "description": "Alert when patient medication adherence drops below 80%",
            "category": "ADHERENCE",
            "severity": "WARNING",
            "condition_logic": {
                "metric": "adherence_percentage",
                "operator": "less_than",
                "threshold": 80.0,
                "timeframe": "weekly"
            },
            "is_active": True,
            "auto_resolve": False,
            "escalation_minutes": 60,
            "notification_methods": ["in_app", "email"],
            "patient_filters": {
                "conditions": ["diabetes", "hypertension"],
                "age_range": {"min": 18, "max": 80}
            }
        }
        
        success3, rule_response = self.run_test(
            "Create Alert Rules",
            "POST",
            "provider/patient-management/alert-rules",
            200,
            data=rule_data
        )
        
        # Validate alert rule response
        if success3 and rule_response:
            expected_keys = ['id', 'provider_id', 'rule_name', 'category', 'severity', 'is_active', 'condition_logic']
            missing_keys = [key for key in expected_keys if key not in rule_response]
            if not missing_keys:
                print(f"   ✅ Alert rule response contains required keys")
                rule_id = rule_response.get('id')
                print(f"   📋 Created rule ID: {rule_id}")
                print(f"   📊 Rule name: {rule_response.get('rule_name', 'N/A')}")
                print(f"   ⚠️ Severity: {rule_response.get('severity', 'N/A')}")
                print(f"   🔄 Active: {rule_response.get('is_active', False)}")
                
                # Check condition logic
                condition_logic = rule_response.get('condition_logic', {})
                if condition_logic:
                    print(f"   🎯 Condition: {condition_logic.get('metric', 'N/A')} {condition_logic.get('operator', 'N/A')} {condition_logic.get('threshold', 'N/A')}")
                
                # Check notification methods
                notification_methods = rule_response.get('notification_methods', [])
                print(f"   📧 Notification methods: {notification_methods}")
            else:
                print(f"   ❌ Alert rule response missing keys: {missing_keys}")
                success3 = False
        
        # Test 4: PUT /api/provider/patient-management/alerts/{alert_id}/acknowledge - Acknowledge alerts
        if alert_id:
            acknowledge_data = {
                "provider_notes": "Contacted patient, discussed medication timing and barriers. Scheduled follow-up in 1 week.",
                "action_taken": "patient_contact_scheduled",
                "follow_up_required": True,
                "follow_up_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
            
            success4, ack_response = self.run_test(
                "Acknowledge Alert",
                "PUT",
                f"provider/patient-management/alerts/{alert_id}/acknowledge",
                200,
                data=acknowledge_data
            )
            
            # Validate acknowledge response
            if success4 and ack_response:
                expected_keys = ['id', 'status', 'acknowledged_at', 'resolution_notes']
                missing_keys = [key for key in expected_keys if key not in ack_response]
                if not missing_keys:
                    print(f"   ✅ Alert acknowledgment response contains required keys")
                    print(f"   🚨 Alert ID: {ack_response.get('id', 'N/A')}")
                    print(f"   📊 Status: {ack_response.get('status', 'N/A')}")
                    print(f"   📅 Acknowledged at: {ack_response.get('acknowledged_at', 'N/A')}")
                    
                    # Check resolution notes
                    resolution_notes = ack_response.get('resolution_notes', '')
                    if resolution_notes:
                        print(f"   📝 Resolution notes: {resolution_notes[:100]}...")
                else:
                    print(f"   ❌ Alert acknowledgment response missing keys: {missing_keys}")
                    success4 = False
        else:
            print("   ⚠️ Skipping alert acknowledgment test - no alert ID available")
            success4 = True  # Don't fail the test if we couldn't get an ID
        
        return success1 and success2 and success3 and success4

    def run_tests(self):
        """Run Phase 2 Patient Management System tests"""
        print("🚀 Starting Phase 2 Patient Management System API Tests...")
        print(f"   Base URL: {self.base_url}")
        print("=" * 80)
        
        # Run Phase 2 tests
        phase2_success = self.test_phase2_patient_management_apis()
        
        # Print final summary
        print("\n" + "=" * 80)
        print(f"📊 FINAL TEST RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 PHASE 2 PATIENT MANAGEMENT SYSTEM RESULTS:")
        print(f"   Overall Success: {'✅ PASSED' if phase2_success else '❌ FAILED'}")
        
        if phase2_success:
            print("🎉 All Phase 2 Patient Management System tests passed!")
            return True
        else:
            print("⚠️ Some Phase 2 tests failed. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  - {result['name']}: {result.get('error', 'Status code mismatch')}")
            return False

if __name__ == "__main__":
    tester = Phase2PatientManagementTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)