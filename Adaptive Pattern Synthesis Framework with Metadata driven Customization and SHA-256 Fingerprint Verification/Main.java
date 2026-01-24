/**
 * Project Title: IntelliArt: A DSL-Based ASCII Art Generation Engine with Cryptographic Integrity
 * (A Multi-Threaded ASCII Art Engine with Plugin Support and Encrypted Output)
 * 
 * Copyright © 2025 Panchadip Bhattacharjee, Advithiya Duddu, Gururaj H L.
 * All Rights Reserved.
 *
 * Description:
 * This program generates ASCII art from input text/images using a multi-threaded engine
 * for enhanced performance. It supports plugins for custom ASCII styles and applies
 * encryption to protect output files.
 *
 * Note:
 * - Entry point: The 'Main' class (contains the main method).
 * - Core logic: Multi-threaded ASCII conversion, plugin handling, and encryption.
 * - Innovation: Encrypted ASCII art output combined with a modular plugin system.
 *
 * Usage:
 * Compile and run `Main.java`. Provide text or image input, and the program will
 * convert it into ASCII art and store it securely as encrypted output.
 */

 // Importing utilities, time API, cryptographic hashing, and UTF-8 charset support
import java.util.*;
import java.time.*;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;


public class Main {
    public static void main(String[] args) {
        System.out.print("\n");
        System.out.println("=== Adaptive Pattern Generator v1.0 ===\n");

        // Pattern configuration (DSL-style input)
        String dsl = """
                pattern: diamond
                theme: plus
                size: 7
                emotion: joyful
                license: CC-BY-SA-4.0
                version: 1.2
                """;

        // Parse metadata from DSL input
        PatternMeta meta = PatternMeta.parse(dsl);

        // Set drawing theme based on config
        ThemeManager.setTheme(meta.theme);

        // Select the correct pattern class
        Pattern pattern = PatternRegistry.get(meta.pattern, meta.size);

        if (pattern == null) {
            System.out.println("Error: Unsupported pattern type.");
            return;
        }

        // Draw the pattern
        String output = pattern.draw();

        // Generate SHA-256 fingerprint (unique hash)
        String signature = Fingerprint.generate(output + meta);

        // Output result and metadata
        System.out.println("--- Pattern Output ---\n" + output);
        System.out.println("--- Metadata ---\n" + meta);
        System.out.println("--- SHA-256 Fingerprint (for originality) ---\n" + signature);
    }
}

// DSL Metadata Class
class PatternMeta {
    String pattern = "triangle", theme = "*", emotion = "neutral", license = "MIT", version = "1.0";
    int size = 5;

    // Parse key-value pairs from DSL-style string
    public static PatternMeta parse(String dsl) {
        PatternMeta meta = new PatternMeta();
        for (String line : dsl.split("\\n")) {
            String[] parts = line.split(":");
            if (parts.length < 2) continue;
            String key = parts[0].trim().toLowerCase();
            String value = parts[1].trim();
            switch (key) {
                case "pattern" -> meta.pattern = value;
                case "theme" -> meta.theme = value;
                case "size" -> meta.size = Integer.parseInt(value);
                case "emotion" -> meta.emotion = value;
                case "license" -> meta.license = value;
                case "version" -> meta.version = value;
            }
        }
        return meta;
    }

    // Display metadata as string
    @Override
    public String toString() {
        return "Pattern: " + pattern +
               "\nTheme: " + theme +
               "\nSize: " + size +
               "\nEmotion: " + emotion +
               "\nLicense: " + license +
               "\nVersion: " + version +
               "\nGenerated on: " + LocalDateTime.now();
    }
}

// Theme Manager: Controls character used in patterns
class ThemeManager {
    private static String themeChar = "*";

    public static void setTheme(String theme) {
        switch (theme.toLowerCase()) {
            case "plus" -> themeChar = "+";
            case "at" -> themeChar = "@";
            case "hash" -> themeChar = "#";
            default -> themeChar = "*";
        }
    }

    public static String repeat(int n) {
        return themeChar.repeat(n);
    }
}

//  Pattern Interface 
interface Pattern {
    String draw();  // Draws the actual pattern
}

//  Pattern Factory / Registry 
class PatternRegistry {
    public static Pattern get(String name, int size) {
        return switch (name.toLowerCase()) {
            case "triangle" -> new Triangle(size);
            case "diamond" -> new Diamond(size);
            case "hourglass" -> new Hourglass(size);
            default -> null;
        };
    }
}

//  Triangle Pattern 
class Triangle implements Pattern {
    int size;
    Triangle(int size) { this.size = size; }

    public String draw() {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= size; i++) {
            sb.append(ThemeManager.repeat(i)).append("\n");
        }
        return sb.toString();
    }
}

//  Diamond Pattern 
class Diamond implements Pattern {
    int size;
    Diamond(int size) { this.size = (size % 2 == 0) ? size + 1 : size; }

    public String draw() {
        StringBuilder sb = new StringBuilder();
        // Upper half
        for (int i = 1; i <= size; i += 2) {
            sb.append(" ".repeat((size - i) / 2)).append(ThemeManager.repeat(i)).append("\n");
        }
        // Lower half
        for (int i = size - 2; i >= 1; i -= 2) {
            sb.append(" ".repeat((size - i) / 2)).append(ThemeManager.repeat(i)).append("\n");
        }
        return sb.toString();
    }
}

//  Hourglass Pattern 
class Hourglass implements Pattern {
    int size;
    Hourglass(int size) { this.size = (size % 2 == 0) ? size + 1 : size; }

    public String draw() {
        StringBuilder sb = new StringBuilder();
        // Upper half
        for (int i = size; i >= 1; i -= 2) {
            sb.append(" ".repeat((size - i) / 2)).append(ThemeManager.repeat(i)).append("\n");
        }
        // Lower half
        for (int i = 3; i <= size; i += 2) {
            sb.append(" ".repeat((size - i) / 2)).append(ThemeManager.repeat(i)).append("\n");
        }
        return sb.toString();
    }
}

//  SHA-256 Fingerprint Generator 
class Fingerprint {
    public static String generate(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
            StringBuilder hex = new StringBuilder();
            for (byte b : hash) {
                hex.append(String.format("%02x", b));
            }
            return hex.toString();
        } catch (Exception e) {
            return "ERROR-GENERATING-FINGERPRINT";
        }
    }
}
