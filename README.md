## 安装 Helm Chart
```
helm install aliyun-billing ./aliyun-billing-exporter -n namespace --create-namespace -f values.yaml
```

## 查看部署
```
kubectl get pods -l app=aliyun-billing-exporter
kubectl get svc aliyun-billing-exporter
```

## 访问 /metrics：
```
kubectl port-forward svc/aliyun-billing-exporter 9105:9105
curl http://localhost:9105/metrics
```


## Prometheus 会自动抓取？

### 如果你使用 Prometheus Operator（kube-prometheus-stack），
并且开启：
```
serviceMonitor:
  enabled: true
```
### Prometheus 会自动发现并开始抓取。

## Dashboard页面
<img width="1581" height="741" alt="image" src="https://github.com/user-attachments/assets/6a194547-654e-42fa-800e-075739ed1d4a" />
<img width="1579" height="634" alt="image" src="https://github.com/user-attachments/assets/c0c58b18-1ba4-4c2d-acfb-8430f63bf03e" />

