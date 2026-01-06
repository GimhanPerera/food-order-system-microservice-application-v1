{{- define "food-ordering.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}

