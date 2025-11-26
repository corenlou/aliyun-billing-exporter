{{/*
Return the name of the chart
*/}}
{{- define "aliyun-billing-exporter.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Create a fully qualified app name
*/}}
{{- define "aliyun-billing-exporter.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else -}}
{{- $name := include "aliyun-billing-exporter.name" . -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end -}}
{{- end }}

{{/*
Standard labels
*/}}
{{- define "aliyun-billing-exporter.labels" -}}
app.kubernetes.io/name: {{ include "aliyun-billing-exporter.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app: {{ include "aliyun-billing-exporter.name" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aliyun-billing-exporter.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aliyun-billing-exporter.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

