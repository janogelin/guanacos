package com.example.ollamaapi.service;

import com.example.ollamaapi.model.ChatRequest;
import com.example.ollamaapi.model.ChatResponse;
import com.example.ollamaapi.model.HealthResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import java.util.*;

/**
 * Service for interacting with the Ollama backend API.
 */
@Service
public class OllamaService {
    private final String OLLAMA_URL = "http://localhost:11434/api/chat";
    private final String OLLAMA_VERSION_URL = "http://localhost:11434/api/version";
    private final String MODEL = "gemma3:4b";

    /**
     * Sends a chat message to the Ollama backend and returns the response.
     */
    public ChatResponse chat(ChatRequest request) {
        RestTemplate restTemplate = new RestTemplate();

        // Build the payload for Ollama
        List<Map<String, String>> messages = new ArrayList<>();
        if (request.getSystemPrompt() != null && !request.getSystemPrompt().isEmpty()) {
            messages.add(Map.of("role", "system", "content", request.getSystemPrompt()));
        }
        messages.add(Map.of("role", "user", "content", request.getMessage()));

        Map<String, Object> payload = new HashMap<>();
        payload.put("model", MODEL);
        payload.put("messages", messages);
        payload.put("stream", false);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(OLLAMA_URL, entity, Map.class);
            Map body = response.getBody();
            if (body != null && body.containsKey("message")) {
                Map message = (Map) body.get("message");
                String content = (String) message.get("content");
                return new ChatResponse(content);
            }
            return new ChatResponse("No response from Ollama server.");
        } catch (Exception e) {
            return new ChatResponse("Error: " + e.getMessage());
        }
    }

    /**
     * Checks the health of the Ollama backend server.
     */
    public HealthResponse healthCheck() {
        RestTemplate restTemplate = new RestTemplate();
        try {
            ResponseEntity<Map> response = restTemplate.getForEntity(OLLAMA_VERSION_URL, Map.class);
            if (response.getStatusCode().is2xxSuccessful()) {
                Map body = response.getBody();
                String version = (body != null && body.containsKey("version")) ? (String) body.get("version") : "unknown";
                return new HealthResponse("ok", "Connected to Ollama " + version);
            }
            return new HealthResponse("error", "Ollama server not healthy");
        } catch (Exception e) {
            return new HealthResponse("error", "Error: " + e.getMessage());
        }
    }
} 