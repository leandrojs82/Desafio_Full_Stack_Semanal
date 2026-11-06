-- Listamos as colunas que vamos preencher.
-- O id fica de fora porque o PostgreSQL vai gerá-lo.
INSERT INTO emprestimo (categoria, data_emprestimo, devolvido)
VALUES
    -- Cada par de parênteses representa um empréstimo.
    -- Os valores seguem a ordem das colunas acima.
    -- A data usa o formato ano-mês-dia.
    -- TRUE e FALSE são valores booleanos escritos sem aspas.

    -- 2 de novembro: Tecnologia devolvido, Literatura em aberto.
    ('Tecnologia', '2026-11-02', TRUE),
    ('Literatura', '2026-11-02', FALSE),

    -- 3 de novembro: História devolvido, Tecnologia em aberto.
    ('História', '2026-11-03', TRUE),
    ('Tecnologia', '2026-11-03', FALSE),

    -- 4 de novembro: os dois empréstimos foram devolvidos.
    ('Literatura', '2026-11-04', TRUE),
    ('Tecnologia', '2026-11-04', TRUE),

    -- 5 de novembro: os dois empréstimos estão em aberto.
    ('História', '2026-11-05', FALSE),
    ('Literatura', '2026-11-05', FALSE),

    -- 6 de novembro: Tecnologia em aberto, História devolvido.
    ('Tecnologia', '2026-11-06', FALSE),
    ('História', '2026-11-06', TRUE),

    -- 7 de novembro: Literatura devolvido, Tecnologia em aberto.
    ('Literatura', '2026-11-07', TRUE),
    ('Tecnologia', '2026-11-07', FALSE);
    -- A vírgula separa os registros. O último termina com ponto e vírgula.