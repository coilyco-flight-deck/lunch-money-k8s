{{- define "lunch-money-k8s.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "lunch-money-k8s.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "lunch-money-k8s.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "lunch-money-k8s.labels" -}}
app.kubernetes.io/name: {{ include "lunch-money-k8s.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end -}}

{{- define "lunch-money-k8s.selectorLabels" -}}
app.kubernetes.io/name: {{ include "lunch-money-k8s.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "lunch-money-k8s.secretName" -}}
{{- if .Values.lunchMoney.existingSecret -}}
{{- .Values.lunchMoney.existingSecret -}}
{{- else -}}
{{- include "lunch-money-k8s.fullname" . -}}
{{- end -}}
{{- end -}}
