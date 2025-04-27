README


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



geoserver:

-Djava.awt.headless=true -Xms4G -Xmx4G -Dgwc.context.suffix=gwc -XX:+UnlockDiagnosticVMOptions -XX:+LogVMOutput -XX:LogFile=/var/log/jvm.log -XX:PerfDataSamplingInterval=500 -XX:SoftRefLRUPolicyMSPerMB=36000 -XX:-UseGCOverheadLimit -XX:ParallelGCThreads=4 -Dfile.encoding=UTF8 -Djavax.servlet.request.encoding=UTF-8 -Djavax.servlet.response.encoding=UTF-8 -Duser.timezone=GMT -Dorg.geotools.shapefile.datetime=false -DGS-SHAPEFILE-CHARSET=UTF-8 -DGEOSERVER_CSRF_DISABLED=true -DPRINT_BASE_URL=https://geonoxt-geoserver-1-1016990259637.us-central1.run.app/geoserver/pdf -DALLOW_ENV_PARAMETRIZATION=true -Xbootclasspath/a:/usr/local/tomcat/webapps/geoserver/WEB-INF/lib/marlin-0.9.3-Unsafe.jar -Dsun.java2d.renderer=org.marlin.pisces.MarlinRenderingEngine
-Djava.awt.headless=true -Xms512m -Xmx1024m -Dgwc.context.suffix=gwc -XX:+UnlockDiagnosticVMOptions -XX:+LogVMOutput -XX:LogFile=/var/log/jvm.log -XX:PerfDataSamplingInterval=500 -XX:SoftRefLRUPolicyMSPerMB=36000 -XX:-UseGCOverheadLimit -XX:ParallelGCThreads=4 -Dfile.encoding=UTF8 -Djavax.servlet.request.encoding=UTF-8 -Djavax.servlet.response.encoding=UTF-8 -Duser.timezone=GMT -Dorg.geotools.shapefile.datetime=false -DGS-SHAPEFILE-CHARSET=UTF-8 -DGEOSERVER_CSRF_DISABLED=true -DPRINT_BASE_URL=https://geonoxt-geoserver-1-1016990259637.us-central1.run.app/geoserver/pdf -DALLOW_ENV_PARAMETRIZATION=true -Xbootclasspath/a:/usr/local/tomcat/webapps/geoserver/WEB-INF/lib/marlin-0.9.3-Unsafe.jar -Dsun.java2d.renderer=org.marlin.pisces.MarlinRenderingEngine


tasks:


aparentemente hay que revisar todo esto:

@app.task

geonode.br.tasks-
geonode.documents.tasks
geonode.geoserver.tasks
geonode.harvesting.tasks
geonode.layers.tasks
geonode.management_commands.tasks
geonode.monitoring.tasks
geonode.tasks.tasks
geonode.upload.tasks
resource.api.tasks

@shared_task
geonode.management_commands_http.tasks
geonode.geoserver.tasks
geonode.monitoring.tasks


