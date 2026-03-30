-- Leemos de SANDBOX y llevamos a INTEGRATION
-- Asumimos que la tabla destino ya existe o se crea con el mismo esquema
MERGE `agatangelo-anton-sandbox1.INTEGRATION.integration_prueba_tecnica` T
USING (
  -- Seleccionamos datos únicos del día
  SELECT DISTINCT id, title, body, userId, CURRENT_DATE() as process_date
  FROM `agatangelo-anton-sandbox1.SANDBOX_mi_app.raw_data`
) S
ON T.id = S.id  -- Si el ID ya existe, actualiza; si no, inserta
WHEN MATCHED THEN
  UPDATE SET T.title = S.title, T.body = S.body
WHEN NOT MATCHED THEN
  INSERT (id, title, body, userId, process_date)
  VALUES (S.id, S.title, S.body, S.userId, S.process_date);
