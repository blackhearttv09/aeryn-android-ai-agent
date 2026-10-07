from __future__ import annotations

from aeryn_core.agent import AerynAgent
from aeryn_core.config import AerynConfig
from aeryn_core.memory import LocalMemory
from aeryn_core.runtime import ExecutionLoop
from aeryn_core.safety import RiskGuard
from aeryn_core.engine import TaskEngine
from mock_automation import MockAutomationEngine


def main() -> None:
    config = AerynConfig.from_env()
    config.ensure_directories()

    memory = LocalMemory(config.db_path)
    agent = AerynAgent(config=config, memory=memory)
    loop = ExecutionLoop(agent)
    risk_guard = RiskGuard(require_confirmation=True)
    task_engine = TaskEngine(config=config, memory=memory)
    automation_engine = MockAutomationEngine(verbose=True)

    print("\n=== Aeryn Agent Started (Mock Mode) ===")
    print(f"Version: 0.1.0")
    mode_str = "Offline Mode" if config.offline_mode else "Online Mode"
    print(f"Mode: {mode_str}")
    print(f"Automation: Mock (No device connected)")
    print()

    # Task 1: Plan and execute opening settings
    goal_1 = "Open Android Settings and take a screenshot"
    print(f"[TASK 1] Goal: {goal_1}")
    plan_1 = loop.run(goal_1, context="User wants to check device settings safely.")
    print(f"Plan Status: {plan_1.get('status')}")
    
    # Execute with mock automation
    print("\n[EXECUTING WITH MOCK AUTOMATION]")
    mock_plan = automation_engine.plan_open_settings()
    result = automation_engine.execute_plan(mock_plan)
    print(f"Execution Result: {result['status']}")
    print()

    # Task 2: Safety check on risky action
    goal_2 = "Send a message to my friend"
    print(f"[TASK 2] Goal: {goal_2}")
    risky_check = risk_guard.evaluate("send a WhatsApp message to Mom", "User wants to contact family")
    print(f"Risky: {risky_check.risky}, Category: {risky_check.category}")
    print(f"Requires Confirmation: {risky_check.requires_confirmation}")
    
    if risky_check.requires_confirmation:
        print("\n[SAFETY GATE] This action requires user confirmation.")
        print("Mock scenario: User confirms the action")
        mock_plan_risky = automation_engine.plan_send_message("Mom", "Hi! Using Aeryn AI")
        result_risky = automation_engine.execute_plan(mock_plan_risky, confirm=True)
        print(f"Execution Result: {result_risky['status']}")
    print()

    # Task 3: Search Play Store
    goal_3 = "Find a task management app on Play Store"
    print(f"[TASK 3] Goal: {goal_3}")
    plan_3 = loop.run(goal_3, context="User wants a productivity app recommendation.")
    print(f"Plan Status: {plan_3.get('status')}")
    
    print("\n[EXECUTING WITH MOCK AUTOMATION]")
    mock_plan_search = automation_engine.plan_search_play_store("task management")
    result_search = automation_engine.execute_plan(mock_plan_search)
    print(f"Execution Result: {result_search['status']}")
    print()

    # Task 4: Full execution report
    execution = task_engine.create_execution(goal_1, "safe device interaction workflow")
    print(f"[TASK EXECUTION REPORT]")
    print(f"Task ID: {execution.task_id}")
    print(f"Status: {execution.status}")
    print(f"Steps: {[step.name for step in execution.steps]}")
    print()

    # Agent final response
    response = agent.respond("Aeryn, what can you help me do on my Android device?")
    print(f"[AGENT RESPONSE]")
    print(response)
    print()

    # Execution history
    print(f"[AUTOMATION HISTORY]")
    history = automation_engine.get_execution_history()
    print(f"Total executed plans: {len(history)}")
    for i, plan in enumerate(history, 1):
        print(f"  {i}. {plan['goal']} - {len(plan['actions'])} actions")
    print()

    print("=== Ready for real device automation ===")
    print("When you connect an Android device via ADB:")
    print("  1. Run 'adb devices' to verify connection")
    print("  2. Switch to automation.py for real device control")
    print("  3. All safety checks remain active")


if __name__ == "__main__":
    main()
