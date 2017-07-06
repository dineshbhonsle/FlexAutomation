#This file holds the variables required for handling convergence
#delays and fault control.

LinkmaxVal = 10     # [In seconds]Maximum time the test retries to bring the port UP.
LinkStepVal = 2     # [In seconds]Step value for which the test sleeps before retrying.
LinkStartVal = 2    # [In seconds]Start value the test should sleep before first check.
Protocol = "http"
Port = "8080"
Headers = """\"Content-Type : application/json\"  --header \"Accept : application/json\""""