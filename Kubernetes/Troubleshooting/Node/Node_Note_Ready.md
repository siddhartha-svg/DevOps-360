# 📉 Kubernetes Node Not Ready - How To Fix It?

Encountering a `NotReady` node in a Kubernetes cluster is a common issue. This guide provides a systematic approach to diagnosing and resolving the problem.

### ⚠️ **What does "NotReady" mean?**

A node's status is managed by the `kubelet` service, which periodically reports the node's health to the control plane. When this communication is interrupted or a health check fails, the control plane marks the node as `NotReady`. This can happen for several reasons, including:

-   **Resource Pressure:** The node is running low on CPU, memory, or disk space.
-   **Kubelet Issues:** The `kubelet` service itself has crashed or is not functioning correctly.
-   **Network Problems:** The node has lost network connectivity to the control plane.
-   **Container Runtime Issues:** The underlying container runtime (e.g., Docker, containerd) is not healthy.

---

### 🔍 **Step-by-Step Diagnosis**

1.  **Identify the Node:**
    First, use `kubectl get nodes` to find which node is in the `NotReady` state.

    ```bash
    kubectl get nodes
    ```

    Example Output:
    ```
    NAME              STATUS     ROLES    AGE   VERSION
    master            Ready      master   51m   v1.31.0
    node-worker-1     NotReady   worker   49m   v1.31.0
    node-worker-2     Ready      worker   47m   v1.31.0
    ```

2.  **Inspect Node Details and Conditions:**
    To understand why the node is `NotReady`, use `kubectl describe node <node-name>`. Pay close attention to the `Conditions` section.

    ```bash
    kubectl describe node node-worker-1
    ```

    Look for specific issues like `MemoryPressure`, `DiskPressure`, or messages indicating that the Pod Lifecycle Event Generator (**PLEG**) is unhealthy.

3.  **Check Network Connectivity:**
    A common cause is a network failure. From the master node, `ping` the `NotReady` node's IP address to check for packet loss.

    ```bash
    ping <node-IP>
    ```

    A 100% packet loss indicates a severe network issue.

4.  **Verify Kubelet Service Status:**
    SSH into the `NotReady` node and check the status of the `kubelet` service.

    ```bash
    systemctl status kubelet
    ```

    If it's not `active (running)`, the `kubelet` service is the likely culprit.

5.  **Examine `kube-proxy` Pods:**
    Check the status of the `kube-proxy` pod on the `NotReady` node, which is essential for network communication.

    ```bash
    kubectl get pods -n kube-system -o wide | grep kube-proxy
    ```

---

### ✅ **How to Fix It**

Based on your diagnosis, follow the appropriate solution.

| Diagnosis                               | Solution                                                                                                                                                             |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Resource Pressure** | **Increase Resources:** Scale up the node or optimize pod resource requests. <br> **Clean Up:** Free up disk space, or stop non-Kubernetes processes on the node.           |
| **Kubelet Issues** | **Restart Kubelet:** Restart the service with `sudo systemctl restart kubelet`. If it fails, check the logs with `sudo cat /var/log/kubelet.log`.                             |
| **`kube-proxy` Issues** | **Check Logs:** Use `kubectl logs <kube-proxy-pod-name> -n kube-system` to find the root cause. <br> **Restart Pod:** Force a restart by deleting the pod. It will be recreated by its DaemonSet. |
| **Network Problems** | **Verify Configuration:** Check firewall rules and network policies. <br> **Test Connectivity:** Use `traceroute` to find where the network path is breaking.                          |

By following these steps, you can effectively pinpoint and resolve the reason behind a `NotReady` Kubernetes node.
