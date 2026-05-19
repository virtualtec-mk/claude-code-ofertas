# UAT - Radar editorial end to end

Fecha: 19/05/2026

- [ ] `radar_editorial` arranca y tiene `RADAR_AGENT_API_TOKEN`.
- [ ] `GET /api/editorial/offers/?store=amazon&limit=10` responde JSON con token.
- [ ] La misma llamada sin token devuelve JSON 401, no login HTML.
- [ ] Una consulta sin resultados devuelve `meta.diagnostics`.
- [ ] `/buscar-ofertas` consume `radar-catalog-client`.
- [ ] Una candidata validada llega a `../claude-code-text-agents/inbox/`.
- [ ] El historial local conserva `radar_offer_id`, `url_origen` y `product_url`.
