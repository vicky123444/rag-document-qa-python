# EKS Troubleshooting Notes

## CrashLoopBackOff investigation

When a pod enters `CrashLoopBackOff`, start by checking the pod status and recent events. First determine whether the application is failing on startup or after a restart.

Use the following commands to gather evidence:

- `kubectl get pod -n <namespace>`
- `kubectl describe pod <pod-name> -n <namespace>`
- `kubectl logs <pod-name> -n <namespace> --previous`
- `kubectl logs <pod-name> -n <namespace> --container <container-name>`

If the container exits immediately, inspect the application logs and environment variables. A common cause is a failing startup command or invalid configuration.

Previous-container logs are especially useful when the container restarts after a crash. They can reveal initialization errors, liveness-probe failures, or missing configuration.
