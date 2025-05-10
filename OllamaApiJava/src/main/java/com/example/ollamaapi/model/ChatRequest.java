package com.example.ollamaapi.model;

/**
 * Request body for the /chat endpoint.
 */
public class ChatRequest {
    private String message;
    private String systemPrompt;

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getSystemPrompt() { return systemPrompt; }
    public void setSystemPrompt(String systemPrompt) { this.systemPrompt = systemPrompt; }
} 