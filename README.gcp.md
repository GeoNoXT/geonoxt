
se agregaron google-cloud-tasks y google-auth en requirements.txt


GCS:




Asegúrate de que tu proyecto de Google Cloud tenga habilitado el servicio de Cloud Tasks. Luego, configura una cola en el archivo queue.yaml o directamente desde la consola de Google Cloud.

Ejemplo de configuración de una cola:

```yaml
queue:
- name: geonoxt-tasks
  rateLimits:
    maxBurstSize: 100
    maxConcurrentDispatches: 1000
    maxDispatchesPerSecond: 500.0
  retryConfig:
    maxAttempts: 100
    maxBackoff: 3600s
    maxDoublings: 16
    minBackoff: 0.100s
  stackdriverLoggingConfig:
    samplingRatio: 1.0
```

aparentemente hay que revisar todo esto:

geonode.br.tasks
geonode.geoserver.tasks
geonode.harvesting.tasks
geonode.layers.tasks
geonode.management_commands.tasks
geonode.monitoring.tasks
geonode.tasks
geonode.upload.tasks