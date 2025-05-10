package com.example.ollamaapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main entry point for the Ollama Gemma Chat API server.
 */
@SpringBootApplication
public class OllamaApiApplication {
    public static void main(String[] args) {
        SpringApplication.run(OllamaApiApplication.class, args);
    }
} 