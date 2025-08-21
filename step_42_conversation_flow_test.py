#!/usr/bin/env python3
"""
STEP 4.2 CONVERSATION FLOW TESTING

Testing the Step 4.2 system in realistic conversation flows to understand
how it handles incomplete responses during different stages of medical interviews.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://mediq-followup.preview.emergentagent.com/api"

def test_conversation_flow(conversation_name, conversation_steps):
    """Test a complete conversation flow"""
    
    print(f"\n🧪 TESTING CONVERSATION FLOW: {conversation_name}")
    print("-" * 60)
    
    # Initialize consultation
    init_response = requests.post(
        f"{BACKEND_URL}/medical-ai/initialize",
        json={
            "patient_id": f"test_patient_{conversation_name.lower().replace(' ', '_')}",
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    if init_response.status_code != 200:
        print(f"❌ Failed to initialize consultation: {init_response.status_code}")
        return False
        
    init_data = init_response.json()
    consultation_id = init_data.get('consultation_id')
    
    if not consultation_id:
        print(f"❌ No consultation ID received")
        return False
    
    print(f"✅ Consultation initialized: {consultation_id}")
    
    conversation_successful = True
    step_results = []
    
    for i, step in enumerate(conversation_steps, 1):
        print(f"\n   Step {i}: User says '{step['message']}'")
        
        # Send message
        message_response = requests.post(
            f"{BACKEND_URL}/medical-ai/message",
            json={
                "message": step['message'],
                "consultation_id": consultation_id,
                "patient_id": f"test_patient_{conversation_name.lower().replace(' ', '_')}",
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if message_response.status_code != 200:
            print(f"   ❌ Failed to send message: {message_response.status_code}")
            conversation_successful = False
            break
            
        response_data = message_response.json()
        response_text = response_data.get('response', '')
        
        # Analyze response
        step_result = {
            "step": i,
            "user_message": step['message'],
            "ai_response": response_text,
            "expected_behavior": step.get('expected_behavior', ''),
            "success": False
        }
        
        # Check if response meets expectations
        if 'expected_indicators' in step:
            found_indicators = []
            for indicator in step['expected_indicators']:
                if indicator.lower() in response_text.lower():
                    found_indicators.append(indicator)
            
            step_result['found_indicators'] = found_indicators
            step_result['success'] = len(found_indicators) > 0
            
            if step_result['success']:
                print(f"   ✅ AI Response: {response_text[:150]}...")
                print(f"   ✅ Found expected indicators: {found_indicators}")
            else:
                print(f"   ❌ AI Response: {response_text[:150]}...")
                print(f"   ❌ Expected indicators not found: {step['expected_indicators']}")
        else:
            # Just check if response is substantial
            step_result['success'] = len(response_text) > 30
            if step_result['success']:
                print(f"   ✅ AI Response: {response_text[:150]}...")
            else:
                print(f"   ❌ AI Response too short: {response_text}")
        
        step_results.append(step_result)
        
        if not step_result['success']:
            conversation_successful = False
        
        time.sleep(1)  # Rate limiting
    
    return {
        "conversation_name": conversation_name,
        "overall_success": conversation_successful,
        "steps": step_results,
        "total_steps": len(conversation_steps),
        "successful_steps": sum(1 for s in step_results if s['success'])
    }

def main():
    """Main testing function"""
    
    print("🚀 STEP 4.2 CONVERSATION FLOW TESTING")
    print("=" * 80)
    
    # Define conversation flows to test
    conversation_flows = [
        {
            "name": "Vague Symptom Follow-up Flow",
            "steps": [
                {
                    "message": "hi",
                    "expected_behavior": "greeting"
                },
                {
                    "message": "I'm not feeling well",
                    "expected_indicators": ["specific symptoms", "what exactly", "describe", "experiencing"],
                    "expected_behavior": "follow-up for vague symptom"
                },
                {
                    "message": "chest pain and nausea",
                    "expected_behavior": "progress to detailed questioning"
                }
            ]
        },
        {
            "name": "Incomplete Pain Description Flow",
            "steps": [
                {
                    "message": "hi",
                    "expected_behavior": "greeting"
                },
                {
                    "message": "chest pain",
                    "expected_indicators": ["what does it feel like", "describe", "crushing", "pressure", "sharp", "quality"],
                    "expected_behavior": "follow-up for incomplete pain"
                },
                {
                    "message": "it's crushing and radiates to my arm",
                    "expected_behavior": "recognize emergency and escalate"
                }
            ]
        },
        {
            "name": "Single Word Anatomical Flow",
            "steps": [
                {
                    "message": "hi",
                    "expected_behavior": "greeting"
                },
                {
                    "message": "chest",
                    "expected_indicators": ["what specific symptoms", "experiencing", "chest pain", "breathing"],
                    "expected_behavior": "follow-up for single word anatomical"
                },
                {
                    "message": "sharp pain when I breathe",
                    "expected_behavior": "detailed symptom collection"
                }
            ]
        },
        {
            "name": "Emotional Response Flow",
            "steps": [
                {
                    "message": "hi",
                    "expected_behavior": "greeting"
                },
                {
                    "message": "scared",
                    "expected_indicators": ["i understand", "what specific", "causing you", "worrying you", "understandable"],
                    "expected_behavior": "empathetic follow-up for emotional response"
                },
                {
                    "message": "I'm worried about my heart symptoms",
                    "expected_behavior": "transition to medical symptom collection"
                }
            ]
        },
        {
            "name": "Temporal Vagueness Flow",
            "steps": [
                {
                    "message": "hi",
                    "expected_behavior": "greeting"
                },
                {
                    "message": "I have a headache",
                    "expected_behavior": "symptom acknowledgment"
                },
                {
                    "message": "recently",
                    "expected_indicators": ["more specific", "hours ago", "days ago", "when exactly", "sudden or gradual"],
                    "expected_behavior": "follow-up for temporal vagueness"
                }
            ]
        }
    ]
    
    # Run all conversation flow tests
    all_results = []
    
    for flow in conversation_flows:
        result = test_conversation_flow(flow["name"], flow["steps"])
        all_results.append(result)
    
    # Generate comprehensive summary
    print("\n" + "=" * 80)
    print("📊 STEP 4.2 CONVERSATION FLOW TESTING SUMMARY")
    print("=" * 80)
    
    total_conversations = len(all_results)
    successful_conversations = sum(1 for r in all_results if r['overall_success'])
    total_steps = sum(r['total_steps'] for r in all_results)
    successful_steps = sum(r['successful_steps'] for r in all_results)
    
    conversation_success_rate = (successful_conversations / total_conversations) * 100 if total_conversations > 0 else 0
    step_success_rate = (successful_steps / total_steps) * 100 if total_steps > 0 else 0
    
    print(f"📋 OVERALL RESULTS:")
    print(f"   Total Conversations: {total_conversations}")
    print(f"   Successful Conversations: {successful_conversations}")
    print(f"   Conversation Success Rate: {conversation_success_rate:.1f}%")
    print(f"   Total Steps: {total_steps}")
    print(f"   Successful Steps: {successful_steps}")
    print(f"   Step Success Rate: {step_success_rate:.1f}%")
    
    print(f"\n📋 CONVERSATION BREAKDOWN:")
    for result in all_results:
        success_rate = (result['successful_steps'] / result['total_steps']) * 100 if result['total_steps'] > 0 else 0
        status = "✅" if result['overall_success'] else "❌"
        print(f"{status} {result['conversation_name']}: {result['successful_steps']}/{result['total_steps']} steps ({success_rate:.1f}%)")
    
    # Analyze Step 4.2 specific functionality
    print(f"\n🎯 STEP 4.2 SPECIFIC ANALYSIS:")
    
    # Count follow-up scenarios
    follow_up_steps = []
    for result in all_results:
        for step in result['steps']:
            if 'expected_indicators' in step:
                follow_up_steps.append(step)
    
    successful_follow_ups = sum(1 for step in follow_up_steps if step['success'])
    follow_up_rate = (successful_follow_ups / len(follow_up_steps)) * 100 if follow_up_steps else 0
    
    print(f"   Follow-up Question Generation: {successful_follow_ups}/{len(follow_up_steps)} ({follow_up_rate:.1f}%)")
    
    # Categorize follow-up types
    follow_up_categories = {
        "Vague Symptoms": 0,
        "Incomplete Pain": 0,
        "Single Word Anatomical": 0,
        "Emotional Responses": 0,
        "Temporal Vagueness": 0
    }
    
    successful_categories = {
        "Vague Symptoms": 0,
        "Incomplete Pain": 0,
        "Single Word Anatomical": 0,
        "Emotional Responses": 0,
        "Temporal Vagueness": 0
    }
    
    for result in all_results:
        for step in result['steps']:
            if 'expected_indicators' in step:
                if "not feeling well" in step['user_message'] or "vague" in result['conversation_name'].lower():
                    follow_up_categories["Vague Symptoms"] += 1
                    if step['success']:
                        successful_categories["Vague Symptoms"] += 1
                elif "pain" in step['user_message'] and "incomplete" in result['conversation_name'].lower():
                    follow_up_categories["Incomplete Pain"] += 1
                    if step['success']:
                        successful_categories["Incomplete Pain"] += 1
                elif len(step['user_message'].split()) == 1 and "anatomical" in result['conversation_name'].lower():
                    follow_up_categories["Single Word Anatomical"] += 1
                    if step['success']:
                        successful_categories["Single Word Anatomical"] += 1
                elif "scared" in step['user_message'] or "emotional" in result['conversation_name'].lower():
                    follow_up_categories["Emotional Responses"] += 1
                    if step['success']:
                        successful_categories["Emotional Responses"] += 1
                elif "recently" in step['user_message'] or "temporal" in result['conversation_name'].lower():
                    follow_up_categories["Temporal Vagueness"] += 1
                    if step['success']:
                        successful_categories["Temporal Vagueness"] += 1
    
    print(f"\n📊 FOLLOW-UP CATEGORY PERFORMANCE:")
    for category in follow_up_categories:
        total = follow_up_categories[category]
        successful = successful_categories[category]
        if total > 0:
            rate = (successful / total) * 100
            status = "✅" if rate >= 80 else "⚠️" if rate >= 60 else "❌"
            print(f"   {status} {category}: {successful}/{total} ({rate:.1f}%)")
    
    # Production readiness assessment
    print(f"\n🚀 STEP 4.2 PRODUCTION READINESS ASSESSMENT:")
    
    # Key metrics
    incompleteness_detection_working = follow_up_rate >= 70
    conversation_flow_maintained = step_success_rate >= 80
    medical_appropriateness = successful_follow_ups > 0
    
    print(f"   {'✅' if incompleteness_detection_working else '❌'} Incompleteness Detection: {follow_up_rate:.1f}% (Target: ≥70%)")
    print(f"   {'✅' if conversation_flow_maintained else '❌'} Conversation Flow: {step_success_rate:.1f}% (Target: ≥80%)")
    print(f"   {'✅' if medical_appropriateness else '❌'} Medical Appropriateness: {'Working' if medical_appropriateness else 'Needs improvement'}")
    
    overall_production_ready = (incompleteness_detection_working and 
                               conversation_flow_maintained and 
                               medical_appropriateness)
    
    if overall_production_ready:
        print(f"\n✅ STEP 4.2 INTELLIGENT FOLLOW-UP SYSTEM IS PRODUCTION-READY")
        print("   - Successfully detects incomplete medical information")
        print("   - Generates appropriate follow-up questions")
        print("   - Maintains conversation flow")
        print("   - Demonstrates medical domain knowledge")
    elif follow_up_rate >= 50:
        print(f"\n⚠️ STEP 4.2 SYSTEM IS FUNCTIONAL BUT NEEDS REFINEMENT")
        print("   - Core follow-up functionality is working")
        print("   - Some incompleteness types need improvement")
        print("   - Conversation flow is mostly maintained")
    else:
        print(f"\n❌ STEP 4.2 SYSTEM NEEDS SIGNIFICANT IMPROVEMENT")
        print("   - Follow-up detection is inconsistent")
        print("   - Multiple conversation flows are failing")
        print("   - System requires debugging and enhancement")
    
    # Save detailed results
    with open('/app/step_42_conversation_flow_results.json', 'w') as f:
        json.dump({
            "summary": {
                "total_conversations": total_conversations,
                "successful_conversations": successful_conversations,
                "conversation_success_rate": conversation_success_rate,
                "total_steps": total_steps,
                "successful_steps": successful_steps,
                "step_success_rate": step_success_rate,
                "follow_up_rate": follow_up_rate,
                "production_ready": overall_production_ready
            },
            "detailed_results": all_results,
            "follow_up_categories": {
                "totals": follow_up_categories,
                "successful": successful_categories
            }
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: /app/step_42_conversation_flow_results.json")
    
    return all_results

if __name__ == "__main__":
    main()