# fdtx-fileshare


Simple Flask file-share app for OpenShift. Features:
- Upload files
- List uploaded files
- Download files
- Delete files


**Namespace:** `fdtx-test`
**PVC:** `fdtx-pvc-fileshare` (40Gi)


## How to use
1. Push this repo to GitHub.
2. In OpenShift, create the project `fdtx-test` (if not exists):
```bash
oc new-project fdtx-test