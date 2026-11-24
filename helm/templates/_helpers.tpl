{{- define "arbiter.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "arbiter.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "arbiter.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "arbiter.labels" -}}
app.kubernetes.io/name: {{ include "arbiter.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "arbiter.selectorLabels" -}}
app.kubernetes.io/name: {{ include "arbiter.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
