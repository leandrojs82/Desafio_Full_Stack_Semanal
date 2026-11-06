-- 1. Lista os empréstimos da data mais antiga para a mais recente.
-- Quando a data é igual, o menor id aparece primeiro.
SELECT *
FROM emprestimo
ORDER BY data_emprestimo, id;

-- 2. COUNT(*) conta todas as linhas da tabela.
SELECT COUNT(*) AS total
FROM emprestimo;

-- 3. WHERE mantém os empréstimos em aberto antes de contar.
SELECT COUNT(*) AS total_em_aberto
FROM emprestimo
WHERE devolvido IS FALSE;

-- 4. GROUP BY reúne as linhas de cada categoria.
-- DESC ordena pela contagem, da maior para a menor.
SELECT categoria, COUNT(*) AS total
FROM emprestimo
GROUP BY categoria
ORDER BY total DESC, categoria;

-- 5. Primeiro filtramos os empréstimos em aberto.
-- Depois contamos as linhas de cada categoria e ordenamos o resultado.
SELECT categoria, COUNT(*) AS total
FROM emprestimo
WHERE devolvido IS FALSE
GROUP BY categoria
ORDER BY total DESC, categoria;
