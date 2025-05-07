-- Importar dados
IMPORT TABLE estacoes FROM "estacoes.csv";
PRINT TABLE estacoes;

-- Criar tabela com base em filtro
CREATE TABLE maiores FROM
  SELECT Local, Coordenadas FROM estacoes
  WHERE Coordenadas < "100"
  LIMIT 5;
PRINT TABLE maiores;

-- Renomear a tabela para outro nome
RENAME TABLE maiores TO estacoes_pequenas;
PRINT TABLE estacoes_pequenas;

-- Criar outra tabela de exemplo
CREATE TABLE top_estacoes FROM
  SELECT Local, Coordenadas FROM estacoes
  WHERE Coordenadas > "200"
  LIMIT 1;
PRINT TABLE top_estacoes;

-- Guardar um procedimento com múltiplos comandos
PROCEDURE nome
BEGIN
  PRINT TABLE estacoes_pequenas;
  PRINT TABLE top_estacoes;
END;

-- Discard (apagar) uma das tabelas
DISCARD TABLE top_estacoes;
PRINT TABLE top_estacoes;

