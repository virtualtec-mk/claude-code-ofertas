# UAT - buscar-ofertas con radar primero

Fecha: 19/05/2026

- [ ] Radar devuelve candidatas suficientes y la skill presenta como maximo 12 con justificacion editorial.
- [ ] Redactor valida una candidata con `product_url`; se invoca `offer-enricher` y se escribe ficha en inbox.
- [ ] Radar devuelve campos incompletos; la skill muestra aviso de calidad.
- [ ] Radar devuelve cero resultados; se escribe diagnostico en `historial/` y no se llama a scrapers locales.
- [ ] Radar inaccesible o token invalido se reporta como error de integracion/configuracion.
- [ ] El historial registra `fuente_descubrimiento: radar_editorial`.
