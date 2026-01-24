import java.util.*;
import java.util.concurrent.*;
import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;
import java.nio.charset.StandardCharsets;
import java.time.*;
import java.lang.reflect.*;

/**
 * Author: Gururaj H.L , Panchadip Bhattacharjee , Advithiya Duddu
 * Project: Dynamic Procedural Art Generator with Multi-Threading,
 *          Plugin Architecture & Encrypted Provenance Tracking
 *
 * Description:
 * Generates complex procedural ASCII art using multi-threading,
 * supports plugin-based pattern algorithms via reflection,
 * and signs output metadata and art with cryptographic hashing and AES encryption.
 */
public class AdvancedArtGenerator {
    public static void main(String[] args) throws Exception {
        System.out.println("=== Dynamic Procedural Art Generator v2.0 ===\n");

        // Sample DSL Configuration (could be extended)
        String config = """
            pattern: fractalTree
            size: 6
            threads: 4
            encryptionKey: SecretKey1234567
            license: GPL-3.0
            version: 2.0
            """;

        Config meta = Config.parse(config);

        // Plugin loader simulation: get pattern class dynamically by name
        PatternPlugin plugin = PluginManager.load(meta.pattern);
        if (plugin == null) {
            System.err.println("ERROR: Pattern plugin not found.");
            return;
        }

        // Multi-threaded art generation
        String art = plugin.generate(meta.size, meta.threads);

        // Metadata info
        String metadata = meta.toString() + "\nGeneratedAt: " + LocalDateTime.now();

        // Combine art + metadata
        String fullOutput = art + "\n\n---METADATA---\n" + metadata;

        // Generate SHA-256 hash
        String hash = CryptoUtil.sha256(fullOutput);

        // Encrypt full output with AES for provenance
        String encrypted = CryptoUtil.aesEncrypt(fullOutput + "\nHASH:" + hash, meta.encryptionKey);

        // Output all
        System.out.println(art);
        System.out.println("--- Metadata & License ---");
        System.out.println(metadata);
        System.out.println("--- SHA-256 Hash ---");
        System.out.println(hash);
        System.out.println("--- Encrypted Provenance (Base64) ---");
        System.out.println(encrypted);
    }
}

// DSL-like config holder
class Config {
    String pattern = "triangle";
    int size = 5;
    int threads = 1;
    String encryptionKey = "defaultkey123456";
    String license = "MIT";
    String version = "1.0";

    static Config parse(String dsl) {
        Config c = new Config();
        for (String line : dsl.split("\\n")) {
            if (!line.contains(":")) continue;
            String[] kv = line.split(":", 2);
            String key = kv[0].trim().toLowerCase();
            String val = kv[1].trim();
            switch (key) {
                case "pattern" -> c.pattern = val;
                case "size" -> c.size = Integer.parseInt(val);
                case "threads" -> c.threads = Integer.parseInt(val);
                case "encryptionkey" -> c.encryptionKey = val;
                case "license" -> c.license = val;
                case "version" -> c.version = val;
            }
        }
        return c;
    }

    @Override
    public String toString() {
        return "Pattern: " + pattern + "\nSize: " + size + "\nThreads: " + threads +
               "\nEncryptionKey: (hidden)" + "\nLicense: " + license + "\nVersion: " + version;
    }
}

// Plugin interface
interface PatternPlugin {
    String generate(int size, int threads) throws Exception;
}

// Plugin Manager with reflection-based loading simulation
class PluginManager {
    static PatternPlugin load(String name) {
        return switch (name.toLowerCase()) {
            case "fractaltree" -> new FractalTree();
            case "cellularautomata" -> new CellularAutomata();
            case "lsystem" -> new LSystemPattern();
            default -> null;
        };
    }
}

// Fractal Tree procedural pattern
class FractalTree implements PatternPlugin {
    private final StringBuilder sb = new StringBuilder();
    private final ExecutorService executor = Executors.newCachedThreadPool();

    @Override
    public String generate(int depth, int threads) throws Exception {
        // Use CountDownLatch to wait for threads
        CountDownLatch latch = new CountDownLatch(1);
        sb.setLength(0);
        // Launch fractal drawing in separate thread
        executor.submit(() -> {
            drawTree(depth, 0);
            latch.countDown();
        });
        latch.await();
        executor.shutdown();
        return sb.toString();
    }

    private void drawTree(int depth, int indent) {
        if (depth == 0) return;
        sb.append(" ".repeat(indent)).append("Y\n");
        // Recursive branching
        drawTree(depth - 1, indent + 2);
        sb.append(" ".repeat(indent)).append("|\n");
        drawTree(depth - 1, indent + 2);
    }
}

// Cellular Automata procedural pattern
class CellularAutomata implements PatternPlugin {
    @Override
    public String generate(int size, int threads) {
        int width = size * 2 + 1;
        int[] current = new int[width];
        int[] next = new int[width];
        current[width / 2] = 1; // single 'on' cell in middle
        StringBuilder sb = new StringBuilder();

        for (int gen = 0; gen < size; gen++) {
            for (int i = 0; i < width; i++) {
                sb.append(current[i] == 1 ? "#" : " ");
            }
            sb.append("\n");
            for (int i = 1; i < width - 1; i++) {
                // Rule 30 example
                next[i] = (current[i - 1] ^ (current[i] | current[i + 1])) & 1;
            }
            current = next.clone();
        }
        return sb.toString();
    }
}

// L-System procedural pattern example
class LSystemPattern implements PatternPlugin {
    private Map<Character, String> rules = Map.of(
        'F', "F+F-F-F+F"
    );

    @Override
    public String generate(int iterations, int threads) {
        String axiom = "F";
        String current = axiom;
        for (int i = 0; i < iterations; i++) {
            StringBuilder next = new StringBuilder();
            for (char c : current.toCharArray()) {
                next.append(rules.getOrDefault(c, "" + c));
            }
            current = next.toString();
        }
        return current;
    }
}

// Cryptography utilities for SHA-256 and AES encryption
class CryptoUtil {
    public static String sha256(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            return "ERROR_SHA256";
        }
    }

    public static String aesEncrypt(String input, String key) {
        try {
            byte[] raw = Arrays.copyOf(key.getBytes(StandardCharsets.UTF_8), 16); // 128-bit key
            SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");

            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(Cipher.ENCRYPT_MODE, skeySpec);

            byte[] encrypted = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(encrypted);
        } catch (Exception e) {
            return "ERROR_AES_ENCRYPT";
        }
    }
}
