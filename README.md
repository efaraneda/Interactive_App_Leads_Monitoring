# Interactive_App_Leads_Monitoring
Construcción de App interactiva para montirear Leads por hora, con un intervalo de confianza, usando Python, Jinja2 y chartJS.
<h2>Gráfico interactivo de referencia para monitorear el KPI deseado como serie temporal por hora. </h2>
<li> Con el código implementado, se logra una proyección de los resultados por hora, usando intervalos de confianza a partir de un valor p de distribución T-student (varianza poblacional desconocida).

![219825373-9d726abe-f961-4519-a28e-019dc63520fe](https://user-images.githubusercontent.com/71103961/219827731-bf8c056d-fac4-4c7e-a729-451c52f7c625.png)

<h2>Observaciones</h2>
<li> El código reajusta automáticamente las proyecciones, cada vez que hay mayor número de datos en la muestra.
<li> En la imagen se ve un N muestral (por hora) igual a 2. Ese es en número de observaciones mínimas para generar los estimadores, pero en teoría, se recomienda usar al menos 28 a 30 observaciones por cada hora.
<li> En otras palabras, idealmente, usar 28 a 30 semanas de datos para que la estimación tenga validez a nivel teórico por Teorema Central del Límite.
<li> Para el dahsboard usé Jinja2 y la librería chart.js, así que es interactivo. El usuario puede ver puntos de datos y ocultar las series.
Dudas/comentarios/aportes a <b>efaraneda@gmail.com</b>
