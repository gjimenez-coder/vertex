# Verificación de fidelidad — better-data-visualizations

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| cap01 | 3 | 1 | 1 | 1 |
| cap02 | 1 | 0 | 0 | 1 |
| cap03 | 0 | 0 | 0 | 0 |
| cap04 | 0 | 0 | 0 | 0 |
| cap05 | 0 | 0 | 0 | 0 |
| cap06 | 0 | 0 | 0 | 0 |
| cap07 | 0 | 0 | 0 | 0 |
| cap08 | 0 | 0 | 0 | 0 |
| cap09 | 1 | 0 | 0 | 1 |
| cap10 | 4 | 0 | 1 | 3 |
| cap11 | 3 | 0 | 2 | 1 |
| cap12 | 0 | 0 | 0 | 0 |
| cap13 | 1 | 0 | 1 | 0 |
| cap14 | 0 | 0 | 0 | 0 |

**Total:** 13 hallazgos (alta 1, media 5, baja 7) en 14 capítulos.

## Detalle

## cap01 — Visual Processing and Perceptual Rankings
Hallazgos: 3 (alta 1, media 1, baja 1)
- [alta] «ángulo; área; volumen; curvatura; y, al final, sombreado/saturación y matiz de color» → "curvatura" no figura en el diagrama de jerarquía perceptiva; es un ítem añadido; evidencia: «Area / Volume / Angle / Parts of a whole / Shading and saturation / Color hue» (PDF p. 29)
- [media] «ángulo; área; volumen» → el orden de la fuente es Área, Volumen, Ángulo; el apunte invierte la posición del ángulo; evidencia: «Area / Volume / Angle» (PDF p. 29)
- [baja] enumeración de la jerarquía → se omite el ítem "Parts of a whole" (partes de un todo) presente en el diagrama; evidencia: «Angle Parts of a whole» (PDF p. 29)

## cap02 — Five Guidelines for Better Data Visualizations
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «el repunte de los 70 a músicos como Neil Young o Neil Diamond» → omite a Neil Sedaka, nombrado en la lista de la fuente; evidencia: «the popularity of musicians like Neil Young, Neil Sedaka, and Neil Diamond in the 1970s» (PDF p. 54)

## cap03 — Form and Function
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap04 — Comparing Categories
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap05 — Time (Tiempo)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap06 — Distribution (Distribución)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap07 — Geospatial (Datos geoespaciales)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap08 — Relationship (Relación)
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap09 — Part-to-Whole (Parte respecto al todo)
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Georgy Voronoi, matemático ruso de finales del siglo XIX» → la fuente lo sitúa en el cambio de siglo (hacia 1900), no a finales del XIX; evidencia: «Georgy Voronoi, a Russian mathematician who lived around the turn of the twentieth century» (PDF p. 304)

## cap10 — Qualitative

Hallazgos: 4 (alta 0, media 1, baja 3)
- [media] «(como en un gráfico de unidades o Isotype, PDF p. 106)» y las demás referencias «PDF p. 179 / p. 206 / p. 277» → son referencias internas del libro a sus páginas impresas ("see page 106", "recall page 179", "page 206", "page 277"), no páginas del PDF; etiquetarlas como «PDF p.» cambia el sentido de la cita; evidencia: «as in a unit or Isotype chart, see page 106» (PDF p. 327)
- [baja] «un conjunto de pequeñas nubes múltiples (siguiendo a Hearst et al., 2019)» → el apunte omite que la summarización semántica del discurso de Obama la hizo USA Today, atribución presente en la fuente; evidencia: «USA Today summarized his speech as follows» (PDF p. 330)
- [baja] «un gráfico de barras con resultados de una encuesta de 2017» en el ejemplo del Texas Tribune → correcto, pero se omite que la fuente llama al conjunto «a bar chart of survey results from a 2017 poll» ligado a seis temas de política; detalle menor de maquetación; evidencia: «a bar chart of survey results from a 2017 poll» (PDF p. 340)
- [baja] «otro ejemplo, basado en entrevistas con cincuenta blogueros de ciencia (Paige Jarreau)» → fiel, pero la fuente nombra a Jarreau solo en el pie de figura, no en el cuerpo; detalle menor de atribución; evidencia: «Paige Jarreau used a word tree to classify interview responses» (PDF p. 333)

## cap11 — Tables (Tablas)
Hallazgos: 3 (alta 0, media 2, baja 1)
- [media] «sparklines (PDF p. 152) para visualizar series» → la fuente cita el número como página del libro ("see page 152"), no como marcador [[PDF p.N]]; etiquetarla «(PDF p. 152)» presenta una referencia interna del libro como cita de página del PDF; evidencia: «you might add sparklines (see page 152) to visualize some data» (PDF p. 350)
- [media] «un heatmap (PDF p. 112)» → mismo problema: la fuente dice "see page 112" (página del libro), no una página del PDF; evidencia: «you could use a heatmap (see page 112) and leave the numbers in the table or hide them» (PDF p. 350)
- [baja] «evita las "oldstyle figures" (números que caen bajo la línea base, como las fuentes Karla, Cabin o Georgia)» → la fuente asocia las oldstyle figures que caen bajo la línea base solo a Georgia; Karla y Cabin se citan por la no-alineación de comas y decimales, no por caer bajo la línea base; evidencia: «commas and decimal points ... don't line up with custom fonts like Karla and Cabin» / «oldstyle figures of Georgia drop some of the digits below the horizontal baseline» (PDF p. 347)

## cap12 — Developing a Data Visualization Style Guide
Hallazgos: 0 (alta 0, media 0, baja 0)

## cap13 — Redesigns (Rediseños)
Hallazgos: 1 (alta 0, media 1, baja 0)
- [media] «las hectáreas cosechadas de cinco cultivos» → la fuente habla de "acres" (acres), no de hectáreas; son unidades distintas; evidencia: «the number of harvested acres for five major crops» (PDF p. 384)

## cap14 — Conclusion (Conclusión)
Hallazgos: 0 (alta 0, media 0, baja 0)
