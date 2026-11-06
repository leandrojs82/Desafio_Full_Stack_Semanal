-- Cria a tabela. Cada linha representará um empréstimo.
CREATE TABLE emprestimo (
    -- ID inteiro. IDENTITY gera o valor quando o INSERT omite o id.
    -- PRIMARY KEY garante que cada empréstimo tenha um id único.
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Categoria do livro, com até 100 caracteres.
    -- NOT NULL torna o preenchimento obrigatório.
    categoria varchar(100) NOT NULL,

    -- DATE guarda a data do empréstimo, sem horário.
    data_emprestimo date NOT NULL,

    -- BOOLEAN guarda TRUE para devolvido e FALSE para em aberto.
    -- NOT NULL garante que todo empréstimo tenha um desses estados.
    devolvido boolean NOT NULL
); -- O ponto e vírgula encerra o comando.