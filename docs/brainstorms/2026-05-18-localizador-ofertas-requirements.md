---
date: 2026-05-18
topic: localizador-ofertas
---

# Localizador de ofertas (estilo claude-code-text-agents)

## Problem Frame

Los redactores ya tienen un sistema de redacción asistida (`claude-code-text-agents`) que funciona y usan a diario. Su cuello de botella actual está **antes** de redactar: encontrar una oferta publicable en Amazon o AliExpress que encaje con la línea editorial del medio para el que escriben. Hoy lo hacen a mano (revisar agregadores, descartar lo que ya está publicado, ver si el precio es real, copiar URL al flujo de redacción).

El objetivo es construir un proyecto hermano local, operado desde Claude Code con comandos, que descubra candidatas, las pase por una validación rápida del redactor y entregue las aprobadas al flujo de redacción existente sin acoplar los dos proyectos.

Aprovechamos las ideas editoriales del antiguo `Proyecto analizador de ofertas` (watchlists, score editorial, validación con motivos estructurados, dedupe) pero descartamos su stack pesado (FastAPI + Postgres + Next.js panel + workers). Todo vive en archivos locales y subagentes en capas, igual que text-agents.

## Requirements

- **R1. Comando de entrada `/buscar-ofertas`.** El redactor lo lanza desde Claude Code, elige **medio**, **anunciante** (Amazon o AliExpress) y **watchlist** opcional. Si no elige watchlist puede describir lo que busca en lenguaje natural ("auriculares ANC alrededor de 60€").
- **R2. Filtro y score guiado por el guideline del medio.** Antes de devolver candidatas, el sistema lee `GUIDELINE-{medio}.md` (mismo archivo que usa text-agents, no se duplica). Categorías cubiertas, marcas afines, rangos de precio y ángulos permitidos filtran y ordenan. Una oferta de juguetes no aparece para un medio que solo cubre deporte y tecnología.
- **R3. Fuente de descubrimiento: agregadores.** El sistema rastrea agregadores tipo Chollometro (lista concreta en planning) filtrando por anunciante. **No** rastrea Amazon/AliExpress directamente como fuente primaria. La URL final guardada sí es la del producto en Amazon/AliExpress (el destino del link del agregador).
- **R4. Búsqueda en dos fases.**
  - *Fase 1 — descubrimiento rápido*: el sistema scrapea el agregador con Playwright MCP y presenta una lista corta (15–25) de candidatas mínimas: título, precio, % descuento, URL de tienda, fuente.
  - *Fase 2 — enriquecimiento al validar*: cuando el redactor marca una candidata como "me interesa", el sistema scrapea la ficha en la tienda (Amazon/AliExpress) para confirmar precio actual, stock, vendedor y características. Solo entonces el redactor toma la decisión final de aceptar o rechazar.
- **R5. Watchlists configurables con afinado conversacional.** Las watchlists son archivos `.md` con frontmatter en `/watchlists/` (nombre, medio sugerido, anunciante, criterios: marcas, categorías, rango de precio, palabras clave). Al lanzarlas el redactor puede afinar en chat ("la de auriculares pero solo Sony y Bose hoy"). El sistema interpreta el afinado como filtros adicionales para esta ejecución, sin tocar el archivo.
- **R6. Validación con motivos estructurados.** Al rechazar una candidata, el redactor elige un motivo de un catálogo cerrado (descuento dudoso, sin stock, ya publicado, marca no alineada, condiciones confusas, otro). Al validar puede añadir una nota libre opcional. Motivos y aceptaciones se persisten para que con el tiempo el sistema aprenda a priorizar mejor (mecanismo de aprendizaje queda fuera del MVP, pero los datos se capturan desde el día 1).
- **R7. Handoff a text-agents vía carpeta compartida.** Cada oferta validada se guarda como un `.md` en una carpeta inbox que text-agents puede leer (ubicación concreta en planning, ej. `claude-code-text-agents/inbox/`). El frontmatter incluye: `url_producto`, `medio`, `anunciante`, `precio_confirmado`, `fecha_validacion`, `fuente_descubrimiento`, ficha enriquecida. El comando `/crear-articulo` del proyecto hermano leerá de esta inbox (modificación menor a coordinar) sin que los proyectos se acoplen en código.
- **R8. Registro local de candidatas trabajadas.** Las ofertas presentadas, rechazadas y validadas quedan en un archivo o carpeta local (`/historial/`) para alimentar dedupe básico y el futuro feedback loop. Las validadas además viven en la inbox compartida hasta que text-agents las consuma.
- **R9. Todo local, sin panel ni DB.** Markdown + Playwright MCP + subagentes. Cero servicios, cero Docker, cero servidor.

## Success Criteria

- Un redactor puede pasar de "tengo que escribir hoy para Mundo Deportivo" a "tengo 3 ofertas validadas en la inbox lista para redactar" en menos de 10 minutos sin salir de Claude Code.
- Las ofertas validadas no requieren re-scraping en text-agents para arrancar la redacción: la ficha enriquecida basta.
- Cero falsos positivos del tipo "el sistema me propuso algo que mi medio nunca publicaría": el filtro por guideline funciona.
- El redactor entiende por qué se le ofrecen las candidatas que se le ofrecen (orden y filtrado explicables en una línea por candidata).

## Scope Boundaries

- **No panel web.** Toda interacción es chat en Claude Code.
- **No DB.** Solo archivos markdown / json locales.
- **No alertas ni scheduling.** El comando se lanza a demanda; nada corre en segundo plano.
- **No validador de precio histórico avanzado.** En MVP, "precio dudoso" depende del agregador y de señales simples (precio actual vs precio tachado en la ficha). Histórico real queda fuera.
- **No copiloto editorial.** Generar titulares, ángulos o cuerpo del artículo es responsabilidad de text-agents. Aquí solo se descubre y valida la oferta.
- **No scraping primario de Amazon/AliExpress.** Solo se entra a la tienda para enriquecer una candidata ya filtrada por el agregador.
- **No multi-medio simultáneo.** Una ejecución del comando trabaja un único par (medio, anunciante). Si el redactor quiere otro medio, lanza el comando de nuevo.
- **No descubrimiento por iniciativa del sistema.** Igual que text-agents: ni Playwright ni ninguna herramienta buscan URLs por su cuenta fuera del comando explícito.

## Key Decisions

- **Agregadores como fuente única de descubrimiento**: aprovechan la curación humana ("esto SÍ está rebajado") y reducen drásticamente la complejidad de scraping frente a entender catálogos completos de tiendas.
- **Búsqueda en dos fases**: evita gastar Playwright en candidatas que el redactor descartaría en 2 segundos por el título.
- **Medio elegido al inicio, no al guardar**: el medio dirige el filtrado, no es una etiqueta posterior. Coherente con la filosofía de text-agents donde el guideline manda desde el principio.
- **Reutilizar `GUIDELINE-{medio}.md` de text-agents en lugar de duplicar**: una sola fuente de verdad editorial para ambos proyectos. Requiere acordar la ruta (`../claude-code-text-agents/guidelines/` o symlink/config).
- **Handoff por carpeta inbox**: desacopla los dos proyectos. text-agents no necesita saber que existe el localizador; solo lee un directorio.
- **Motivos de rechazo cerrados desde el día 1**: aunque el aprendizaje automático no exista en MVP, los datos limpios desde el inicio permiten habilitarlo después sin migrar.

## Dependencies / Assumptions

- Playwright MCP ya está instalado y operativo en el entorno del redactor (es prerrequisito de text-agents también).
- El proyecto `claude-code-text-agents` está en una ruta accesible localmente desde este proyecto. Se asumirá una raíz común `proyectos-IA/` salvo configuración explícita.
- Los redactores ya saben cómo lanzar comandos slash en Claude Code (text-agents en producción).
- Modificar `/crear-articulo` de text-agents para que lea de una inbox es aceptable y de bajo coste (no se hace en este proyecto, se coordina).

## Outstanding Questions

### Resolve Before Planning

_Ninguna. Las decisiones de producto están cerradas._

### Deferred to Planning

- [Afecta R3][Needs research] Qué agregadores concretos del día 1. Chollometro es el candidato obvio para España; conviene revisar Compradicción, NoTengoSuelto y cualquier otro con buen filtro por tienda. Decisión basada en facilidad de scraping con Playwright y calidad del filtro Amazon/AliExpress.
- [Afecta R7][Técnico] Ruta exacta de la inbox compartida y formato definitivo del frontmatter. Hay que acordarlo con la estructura actual de text-agents (`/drafts/`, `/guidelines/`) para encajar sin romper convenciones.
- [Afecta R8][Técnico] Mecanismo de dedupe / "ya publicado". Opciones: histórico propio en `/historial/`, leer drafts publicados de text-agents, o ambos. Depende de si text-agents marca drafts como publicados (hoy probablemente no).
- [Afecta R2, R6][Técnico] Arquitectura de subagentes en capas, paralela a la de text-agents. Probable división: `aggregator-scraper`, `editorial-filter`, `store-enricher`, `validation-orchestrator`. A definir en planning con qué fuentes lee cada uno.
- [Afecta R5][Técnico] Esquema concreto del frontmatter de watchlist y catálogo inicial de watchlists para los medios actuales (`mundodeportivo`, `larazon`).
- [Afecta R4][Needs research] Estrategia para captchas / bloqueos en Amazon al enriquecer (R4 fase 2). En text-agents hay `URLBlockedError` que cae a flujo manual; aquí conviene replicar el mismo patrón.

## Next Steps

→ `/ce:plan` para planificar la implementación.
