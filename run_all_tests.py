import os
import subprocess
import sys

def run_tests():
    test_dir = "tests"
    files = sorted([f for f in os.listdir(test_dir) if f.endswith(".js")])
    
    passed_count = 0
    failed_count = 0
    
    print(f"Running {len(files)} test files...\n")
    print(f"{'Test File':<30} | {'Status':<10}")
    print("-" * 45)
    
    for filename in files:
        filepath = os.path.join(test_dir, filename)
        
        # Run with node
        node_res = subprocess.run(["node", filepath], capture_output=True, text=True)
        node_out = node_res.stdout.strip()
        node_err = node_res.stderr.strip()
        
        # Run with our python interpreter
        py_res = subprocess.run(["python", "main.py", filepath], capture_output=True, text=True)
        py_out = py_res.stdout.strip()
        py_err = py_res.stderr.strip()
        
        if node_res.returncode != 0:
            # If node fails, it might be an invalid test or node error
            print(f"{filename:<30} | SKIP (Node failed: {node_err})")
            continue
            
        if py_res.returncode != 0:
            print(f"{filename:<30} | FAIL (Python exited with {py_res.returncode})")
            print(f"--- Python stderr ---")
            print(py_err)
            print("-" * 20)
            failed_count += 1
            continue
            
        if node_out == py_out:
            print(f"{filename:<30} | PASS")
            passed_count += 1
        else:
            print(f"{filename:<30} | FAIL (Output mismatch)")
            print(f"--- Expected (Node) ---")
            print(repr(node_out))
            print(f"--- Actual (Python) ---")
            print(repr(py_out))
            print("-" * 20)
            failed_count += 1
            
    print("-" * 45)
    print(f"Total: {passed_count + failed_count} | Passed: {passed_count} | Failed: {failed_count}")
    return failed_count == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
