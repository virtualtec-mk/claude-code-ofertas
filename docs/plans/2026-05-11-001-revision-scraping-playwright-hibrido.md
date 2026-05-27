# Revisión del scraping: Playwright como capa principal con fallback manual

- **Fecha de creación:** 11/05/2026
- **Autor:** Claude (Opus 4.7) bajo dirección del redactor
- **Estado:** Borrador para aprobación
- **Reemplaza:** sección "URLBlockedError" del plan original `2026-05-08-001`

---

## 1. Problema

`product-researcher` usa hoy `WebFetch` como única vía para extraer la ficha del producto. En la práctica:

- **Amazon (.es / .com)** devuelve HTML mínimo o redirección a captcha cuando detecta cliente no-navegador. Tasa de éxito observada: baja.
- **AliExpress** devuelve placeholders renderizados por JavaScript (la página real se hidrata en el cliente). `WebFetch` recibe markup vacío.
- El fallback `URLBlockedError` (pedir al redactor que pegue la ficha a mano) deja de ser excepción y pasa a ser el flujo habitual. Eso rompe la promesa del producto: "pega la URL y recibe el artículo".

## 2. Decisión

Adoptar enfoque **híbrido** confirmado por el redactor:

1. `product-researcher` intenta primero **Playwright MCP** (navegador real, ejecución de JS, espera a hidratación).
2. Si Playwright falla (captcha, timeout, plugin no disponible) → degradar al flujo manual actual (`URLBlockedError`).
3. La degradación es transparente y rápida: el redactor nunca espera más de ~20s antes de saber si tiene que pegar los datos a mano.

## 3. Tradeoffs aceptados

| Aspecto | Antes (WebFetch) | Después (Playwright + fallback) |
|---|---|---|
| Tasa de éxito automática Amazon | ~20-40% | esperado 70-90% |
| Tasa de éxito automática AliExpress | ~0-10% | esperado 50-70% (captchas siguen apareciendo) |
| Latencia por producto | 1-3s | 5-15s |
| Dependencia técnica | Ninguna | Plugin `@playwright/mcp` instalado en Claude Code del redactor |
| Coste por sesión | Bajo | Mayor (más tokens de DOM, screenshots) |

El redactor acepta la latencia y el coste a cambio de dejar de pegar datos manualmente en la mayoría de casos.

## 4. Cambios en el sistema

### 4.1 Subagente `product-researcher`

Editar `.claude/agents/product-researcher.md`:

- **`tools:`** añadir las tools del plugin Playwright que vamos a usar:
  - `mcp__plugin_playwright_playwright__browser_navigate`
  - `mcp__plugin_playwright_playwright__browser_snapshot`
  - `mcp__plugin_playwright_playwright__browser_wait_for`
  - `mcp__plugin_playwright_playwright__browser_take_screenshot` (opcional, para capturar precio si el snapshot no es suficiente)
  - `mcp__plugin_playwright_playwright__browser_close`
  - Eliminar `WebFetch` del subagente. Con la política actual de dominios (Amazon + AliExpress), no queda ningún caso en el que WebFetch sea útil; mantenerlo invita a confusión.
  - Mantener `Read`.

- **Nueva sección "Estrategia de extracción"** que reemplaza el "Paso 1" actual:

  1. **Flujo único Playwright** (todas las URLs autorizadas pasan por aquí):
     - `browser_navigate` a la URL.
     - `browser_wait_for` esperando un **patrón de precio** en la página (regex tipo `\d+[.,]\d{2}\s*€` o equivalente para `$`/`£`), con timeout de 10s. Es más estable entre locales y A/B tests que esperar a un CTA tipo "Añadir al carrito".
     - `browser_snapshot` para obtener el accessibility tree estructurado.
     - Si el snapshot no contiene precio detectable → `browser_take_screenshot` y leer el precio del propio screenshot (fallback visual).
     - `browser_close` al final. Si una extracción posterior detecta sesión sucia (cookies/captcha residual), reabrir sesión limpia. Aceptamos que en un agente prompt-based no hay try/finally garantizado.
  2. **Detección de captcha / bloqueo:** si el snapshot contiene textos como "captcha", "robot", "verify you're human", "API-HTTP-403", o si el `wait_for` agota timeout → tratar como `URLBlockedError` y degradar al flujo manual.

- **Sección `URLBlockedError`** se mantiene tal cual: ahora es la red de seguridad cuando Playwright también falla.

- **Frontmatter de output:** el campo `fuente` pasa a tener dos valores: `automatica-playwright | manual`. Actualizar tanto el frontmatter del agente como el bloque de output de ejemplo (el que hoy declara `fuente: "[automatica | manual]"` en el agente). Útil para depurar después qué método tuvo éxito.

### 4.2 Documentación para el redactor

Crear `docs/instalacion-playwright.txt` (formato txt simple, según CLAUDE.md global) con:

- Qué es el plugin de Playwright y por qué se necesita.
- Comando exacto para instalarlo en Claude Code (a confirmar con la documentación oficial del plugin).
- **Versión recomendada del plugin** (pinear para que un cambio de nombres de tools no rompa el subagente en silencio). Documentar también cómo actualizar de forma controlada.
- Aviso de que al ejecutarse abrirá una ventana de Chrome visible durante unos segundos. Es comportamiento esperado, no hace falta headless.
- Cómo verificar que está activo (`/plugins` o equivalente).
- Qué hacer si no se puede instalar (el sistema sigue funcionando, solo se cae más a menudo al flujo manual).

### 4.3 Actualización de `CLAUDE.md` del proyecto

- Añadir Playwright a la lista de dependencias en una nueva subsección "Requisitos del entorno".
- Actualizar la sección "Política de uso de WebFetch" → renombrarla a "Política de uso de herramientas de scraping" e incluir las nuevas tools de Playwright bajo las mismas reglas (solo URLs pegadas por el redactor, dominios autorizados, nunca descubrir URLs).
- Actualizar la sección `URLBlockedError` para reflejar que ahora se dispara solo después de que Playwright también haya fallado.

### 4.4 Changelog

Añadir entrada en `/changelog/` con fecha 11/05/2026 documentando:
- Motivación (anti-scrapers de Amazon/AliExpress).
- Cambio (Playwright como vía principal, fallback manual).
- Impacto en el redactor (necesita instalar plugin).

## 5. Criterios de aceptación

- [ ] Una URL de Amazon.es de un producto en oferta se extrae correctamente sin intervención manual en al menos 4 de cada 5 intentos.
- [ ] Una URL de AliExpress se extrae sin intervención manual en al menos 1 de cada 2 intentos (somos realistas: AliExpress es más hostil).
- [ ] Cuando Playwright falla, el redactor recibe el mensaje de `URLBlockedError` en menos de 20s desde que pegó la URL.
- [ ] El frontmatter del output indica correctamente qué método se usó (`fuente`).
- [ ] Existe `docs/instalacion-playwright.txt` con instrucciones claras para un perfil no técnico.

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Plugin Playwright no disponible en la sesión del redactor | El subagente debe detectar el error "tool not available" y degradar inmediatamente a `URLBlockedError` sin reintentar. |
| Captchas persistentes en AliExpress | Aceptado. El fallback manual cubre el caso. No invertir en bypass de captcha (ético y técnicamente complicado). |
| Sesiones de navegador que no se cierran | Llamar `browser_close` siempre, incluso en rama de error. |
| Tokens consumidos por DOM grandes | Usar `browser_snapshot` (accessibility tree, ya filtrado) en lugar de leer HTML crudo. Reservar el screenshot solo para cuando el snapshot no tiene el precio. |
| Cambio de selectores/textos en Amazon-AliExpress en el futuro | El subagente extrae por contenido del snapshot (precio, nombre), no por selectores CSS. Es robusto frente a cambios de maquetación. |

## 7. Fuera de alcance

- No vamos a implementar bypass de captcha, rotación de proxies, ni stealth fingerprinting.
- No vamos a cachear resultados de productos entre sesiones (cada extracción es fresca).
- No vamos a soportar tiendas adicionales en este cambio (PCComponentes, MediaMarkt, etc. ya estaban contempladas en la sección "otras tiendas" del agente original — siguen igual).

## 8. Pasos de implementación (cuando se apruebe el plan)

1. Editar `.claude/agents/product-researcher.md` con la nueva estrategia y tools.
2. Crear `docs/instalacion-playwright.txt`.
3. Actualizar `CLAUDE.md` (secciones de scraping y excepciones).
4. Añadir entrada en `/changelog/`.
5. Probar manualmente con **5 URLs de Amazon y 5 de AliExpress** (mínimo necesario para validar los ratios de los criterios de aceptación). Registrar resultado de cada intento (éxito automático / fallback manual / error) para poder calcular el ratio.
6. Si los criterios de aceptación se cumplen, marcar plan como completado.
