package com.example.ollamaapi.controller;

import com.example.ollamaapi.model.ChatRequest;
import com.example.ollamaapi.model.ChatResponse;
import com.example.ollamaapi.model.HealthResponse;
import com.example.ollamaapi.service.OllamaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

/**
 * REST controller for chat and health endpoints.
 */
@RestController
@RequestMapping("/")
@Tag(name = "Ollama Gemma Chat API", description = "Endpoints for chatting with the Gemma model and health checks.")
public class ChatController {

    @Autowired
    private OllamaService ollamaService;

    @PostMapping("/chat")
    @Operation(summary = "Chat with the Gemma model", description = "Send a chat message to the Ollama (Gemma) model and receive a response.")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        return ollamaService.chat(request);
    }

    @GetMapping("/healthz")
    @Operation(summary = "Health check", description = "Check if the Ollama server and model are available.")
    public HealthResponse healthz() {
        return ollamaService.healthCheck();
    }
} 