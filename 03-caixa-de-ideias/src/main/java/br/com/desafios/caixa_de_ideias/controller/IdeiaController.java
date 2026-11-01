package br.com.desafios.caixa_de_ideias.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.desafios.caixa_de_ideias.repository.IdeiaRepository;
import jakarta.validation.Valid;
import br.com.desafios.caixa_de_ideias.dto.CriarIdeiaRequest;
import br.com.desafios.caixa_de_ideias.model.Ideia;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;




@RestController 
@RequestMapping("/ideias")
public class IdeiaController {

    private final IdeiaRepository repository;

    // O Spring fornece o repositório ao criar este controller
    public IdeiaController(IdeiaRepository repository){
        this.repository = repository;
    }
    
    // Atende GET /ideias e retorno todos os registros.
    @GetMapping
    public List<Ideia> listar(){
        return repository.findAll();
    }

    @PostMapping
    public ResponseEntity<Ideia> cadastrar(
        @Valid @RequestBody CriarIdeiaRequest request){

            // Criar a entidade usando o título recebido no JSON
            Ideia ideia = new Ideia();
            ideia.setTitulo(request.titulo());

            // Salva no banco e recebe a entidade com o identificardor gerado.
            Ideia salva = repository.save(ideia);

            // Responde com status 201, endereço do recurso e dados salvos
            return ResponseEntity
            .created(URI.create("/ideias/" + salva.getId()))
            .body(salva);

        }

        // Atende, por exemplo, GET /ideias/1.
        @GetMapping("/{id}")
        public ResponseEntity<Ideia> buscarPorId(@PathVariable Long id){
            //Retorna 200 com a ideia, ou 404 quando ela não existe.
            return ResponseEntity.of(repository.findById(id));
        }
    
}
