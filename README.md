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
<img width="1581" height="741" alt="image" src="https://github.com/user-attachments/assets/046a8830-8923-49a7-afb9-5a32517de8c3" />
<img width="1579" height="634" alt="image" src="https://github.com/user-attachments/assets/70138971-0c49-4b4a-ab33-af385c127807" />



