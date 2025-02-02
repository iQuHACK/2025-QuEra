import os
import subprocess

def run_files(directory='.'):
    python_files = [f for f in os.listdir(directory) if f[0].isdigit() and f.endswith('.py')]

    python_files.sort()

    for file in python_files:
        print(f"\n{'='*50}")
        print(f"Running: {file}")
        print(f"{'='*50}")

        try:
            result = subprocess.run(['python', os.path.join(directory, file)],
                    capture_output=True,
                    text=True)

            if result.stdout:
                print("Output:")
                print(result.stdout)

            if result.stderr:
                print("Errors:")
                print(result.stderr)

        except Exception as e:
            print(f"Error running {file}: {str(e)}")
            

if __name__ == "__main__":
    run_files()
        
