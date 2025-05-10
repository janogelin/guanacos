package com.example.ollamaapi.config;

import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.OpenAPI;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OpenAPI configuration for Swagger UI metadata.
 */
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Ollama Gemma Chat API")
                .version("1.0.0")
                .description("A REST API for interacting with the Ollama (Gemma) language model. Accepts chat messages and returns model responses.")
            );
    }
} 