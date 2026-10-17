# Kubernetes Debugging Checklist

## Investigating pod restarts

When a pod restarts repeatedly, check the container status and review the latest events. Runtime errors, image-pull failures, and invalid mount paths are among the common Kubernetes issues.

The goal is to identify whether the application is unhealthy, the container cannot start, or the pod is blocked by a configuration problem. If the app crashes after startup, inspect the logs from the most recent run and compare them with the previous container logs.

A useful debugging process includes:

1. Describe the pod to review conditions and warnings.
2. Inspect resource requests and limits.
3. Read container logs for startup exceptions.
4. Verify configuration values and secret references.
5. Verify readiness and liveness probes.

This process helps narrow the root cause and reduces guesswork during incident response.
