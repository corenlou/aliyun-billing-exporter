## 自定义value.yaml配置
### 配置镜像版本
```
image:
  repository: devocenter/aliyun-billing-exporter
  tag: latest 
  pullPolicy: IfNotPresent
```
### 配置副本数
```
replicaCount: 1
```
### 配置脚本参数
```
env:
  ## 如果所有的账号都是国际账号则统一写ap-southeast-1，
  ## 如果都是大陆账号则填写cn-hongzhou,
  ## 如果是大陆和国际账号混用的话，则需要和下面的secret配置一样填多了一分号";"隔离 例如："ap-southeast-1;cn-hangzhou;cn-hangzhou"
  region: "ap-southeast-1"
  ## 自定义从哪个月开始统计费用，时间不宜过长，数据量越大影响服务器资源，数据量太大受prometheus和serviceMonitor scrapeTimeout时间影响
  month: "2025-09"
  ## 自定义账号名称，可以根据项目来自定
  account: "A;B;C"
```
### 配置阿里云账号ACCESSSKEY和SECRETKEY，多账号以分号";"分隔
```
secret:
  ## 注意一一对应
  accessKey: "AAA;BBB;CCC" 
  secretKey: "secret1;secret2;secret3"
```
### 自定义port
```
service:
  port: 9105
  type: ClusterIP
```
### 限制资源
```
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi
```
## 安装 Helm Chart
```
cd helm
helm install aliyun-billing . -n namespace --create-namespace --set.image.tag=latest -f values.yaml
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
开启servicemonitor并且更改serviceMonitor超时时间：
```
serviceMonitor:
  ### 开启serviceMonitor
  enabled: true
  #### 抓取间隔
  interval: 60s
  #### 抓取超时时间
  scrapeTimeout: 20s
```
### Prometheus 会自动发现并开始抓取。

## Dashboard页面
<img width="1581" height="741" alt="image" src="https://github.com/user-attachments/assets/046a8830-8923-49a7-afb9-5a32517de8c3" />
<img width="1579" height="634" alt="image" src="https://github.com/user-attachments/assets/70138971-0c49-4b4a-ab33-af385c127807" />

## dockerhub
[devocenter/aliyun-billing-exporter](https://hub.docker.com/r/devocenter/aliyun-billing-exporter/tags)

