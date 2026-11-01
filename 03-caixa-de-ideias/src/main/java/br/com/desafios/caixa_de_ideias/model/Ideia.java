package br.com.desafios.caixa_de_ideias.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import org.hibernate.annotations.Bag;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity 
public class Ideia {

    @Id 
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "O título é obrigatorio")
    @Size(max = 100, message = "O título deve ter no máximo 100 caracteres")
    private String titulo;

    // Permite Consultar o identificador.
    public Long getId(){
        return id;
    }

    // Permite consultar o titulo.
    public String getTitulo(){
        return titulo;
    }

    // Permite definir ou alterar o titulo;
    public void setTitulo(String titulo){
        this.titulo = titulo;
    }
}