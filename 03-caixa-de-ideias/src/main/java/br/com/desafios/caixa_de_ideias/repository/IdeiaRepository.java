package br.com.desafios.caixa_de_ideias.repository;

import br.com.desafios.caixa_de_ideias.model.Ideia;
import org.springframework.data.jpa.repository.JpaRepository;

public interface IdeiaRepository extends JpaRepository<Ideia, Long> {
    
}
