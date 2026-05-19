# Notas de degradación

Log libre de dominios y patrones problemáticos detectados durante el scraping. Cada nota: fecha (DD/MM/YYYY), dominio, síntoma, mitigación aplicada o pendiente.

Formato sugerido por entrada:

```
## DD/MM/YYYY — dominio.tld
- Síntoma: [qué falló: captcha, timeout, selector roto, redirect nuevo...]
- Contexto: [qué intentaba hacer el subagente]
- Mitigación: [qué se cambió, o "pendiente"]
```

---

## Selectores y URLs de Chollometro — SCOUT 19/05/2026

**Estado: VALIDADO EN VIVO el 19/05/2026** con Playwright MCP. Los valores siguientes están reflejados en `.claude/agents/aggregator-scraper.md`. Si cambian, actualiza AMBOS sitios.

### URLs base por anunciante (validadas)

- Amazon España: `https://www.chollometro.com/search/ofertas?merchant-id=173`
- AliExpress España: `https://www.chollometro.com/search/ofertas?merchant-id=165`

**Desviación clave:** el patrón antiguo `/grupo/<tienda>` devuelve 404 desde 2026. Sustituido por `/search/ofertas?merchant-id=<N>`. Los merchant-id se obtienen buscando la tienda en `/search?q=<tienda>` y clicando el link "Tienda de <X>" en el panel "Relacionado".

### Selectores accesibles (validados)

- Item de oferta: rol **`article`** (sin nombre accesible propio).
- Título: primer `link` interno al article, envuelto en `<strong>`. El href apunta a `/ofertas/<slug>` (página de detalle dentro de Chollometro).
- Precio actual: primer `generic` con patrón `\d+[.,]\d{2}\s*€` dentro del bloque de precios.
- Precio anterior tachado: segundo `generic` con el mismo patrón, inmediatamente después del actual.
- Porcentaje descuento: `generic` con patrón `-XX%` en el mismo bloque (tercera posición).
- Botón a tienda: rol `button` con nombre accesible literal **"Ir al chollo"** (no "Ir a la oferta" como decía el spec inicial).

### Banner de cookies (validado)

- Aparece solo en la primera navegación de la sesión.
- Botón de aceptación: rol `button`, nombre accesible literal **"Aceptar todo"**.

### Mecánica del redirect de afiliación (validada)

El click en "Ir al chollo" **abre una pestaña NUEVA** directamente en la URL final de la tienda (no navega en la misma pestaña, no hay redirect intermedio observable, no hace falta `browser_evaluate` ni `browser_network_requests`).

- Estrategia simple (válida hoy):
  1. `browser_click` sobre "Ir al chollo".
  2. Leer la URL de la nueva pestaña en el output del propio click (sección "Open tabs").
  3. Filtrar dominio: aceptar solo `amazon.es` o `es.aliexpress.com`; cualquier otro dominio → descartar candidata.
  4. La URL incluye tag de afiliado (`tag=pepperugc-21&ascsubtag=...`); para `url_canonica` truncar al patrón limpio `amazon.es/dp/<ASIN>` o `es.aliexpress.com/item/<ID>.html` si reconocible.
- Ejemplo real capturado: `https://www.amazon.es/dp/B0DFQCQDNZ?tag=pepperugc-21&ascsubtag=ppr-es-984824478` → limpia: `https://www.amazon.es/dp/B0DFQCQDNZ`.
- Alternativa si la pestaña nueva no expone la URL: `browser_evaluate("() => location.href")` tras 8 s o `browser_network_requests`.

### Paginación

`?page=N` añadido a la URL base (no verificado en el scout; asumir por convención Pepper hasta confirmar). MVP usa solo página 1.

---

## Fuentes alternativas (referencia, NO activas en MVP)

(Las dos de Telegram se promovieron a fuentes activas el 19/05/2026; ver `fuentes.md` y `.claude/agents/telegram-scraper.md`. Quedan aquí solo las que siguen en reserva.)

- **Compradicción** — agregador editorial activo en 2026. Candidata si Chollometro endurece anti-bot o cambia de modelo.

---

## Entradas reales

_(Vacío — se irá rellenando con las observaciones de cada sesión problemática.)_
