package main

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
    "time"
    "log"
)

type Platform struct {
    Name   string `json:"name"`
    URL    string `json:"url"`
    Found  bool   `json:"found"`
}

type ExecResult struct {
    Username  string     `json:"username"`
    ExitCode  int        `json:"exit_code"`
    Platforms []Platform `json:"platforms"`
    RawOutput string     `json:"raw_output"`
    Stderr    string     `json:"stderr"`
}

func installGosearch(ctx context.Context) error {
    // Use the current environment so Dockerfile-provided GOBIN/GOPATH are respected.
    cmd := exec.CommandContext(ctx, "go", "install", "github.com/ibnaleem/gosearch@latest")
    cmd.Env = os.Environ()
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    return cmd.Run()
}

func gosearchPath() (string, error) {
    // Use GOBIN if set, otherwise GOPATH/bin
    gobin := strings.TrimSpace(os.Getenv("GOBIN"))
    if gobin != "" {
        return filepath.Join(gobin, "gosearch"), nil
    }

    gopathOut, err := exec.Command("go", "env", "GOPATH").Output()
    if err != nil {
        return "", err
    }
    gopath := strings.TrimSpace(string(gopathOut))
    return filepath.Join(gopath, "bin", "gosearch"), nil
}

func stripANSI(str string) string {
    // Remove ANSI escape codes
    ansiRegex := strings.NewReplacer(
        "\u001b[93m", "",
        "\u001b[92m", "",
        "\u001b[91m", "",
        "\u001b[0m", "",
    )
    result := ansiRegex.Replace(str)
    
    // Remove any remaining escape sequences
    for strings.Contains(result, "\u001b") {
        start := strings.Index(result, "\u001b")
        if start == -1 {
            break
        }
        end := start + 1
        for end < len(result) && result[end] != 'm' {
            end++
        }
        if end < len(result) {
            result = result[:start] + result[end+1:]
        } else {
            break
        }
    }
    
    return result
}

func parseGosearchOutput(output string) []Platform {
    var platforms []Platform
    lines := strings.Split(output, "\n")
    
    for _, line := range lines {
        line = stripANSI(line)
        line = strings.TrimSpace(line)
        
        // Skip empty lines, headers, and info lines
        if line == "" || 
           strings.HasPrefix(line, "::") || 
           strings.HasPrefix(line, "[*]") ||
           strings.HasPrefix(line, "⎯") ||
           strings.HasPrefix(line, "[!]") ||
           strings.HasPrefix(line, "┌") ||
           strings.HasPrefix(line, "├") ||
           strings.HasPrefix(line, "└") ||
           strings.HasPrefix(line, "│") ||
           strings.Contains(line, "___") ||
           strings.Contains(line, "Number of profiles") ||
           strings.Contains(line, "Total time taken") {
            continue
        }
        
        // Look for platform result lines with [+] or [?] markers
        if (strings.HasPrefix(line, "[+]") || strings.HasPrefix(line, "[?]")) && strings.Contains(line, "http") {
            // Remove the status marker
            line = strings.TrimPrefix(line, "[+]")
            line = strings.TrimPrefix(line, "[?]")
            line = strings.TrimSpace(line)
            
            // Split by colon to get platform name and URL
            parts := strings.SplitN(line, ":", 2)
            if len(parts) >= 2 {
                platformName := strings.TrimSpace(parts[0])
                url := strings.TrimSpace(parts[1])
                
                // Ensure URL starts with http
                if strings.HasPrefix(url, "http") {
                    platforms = append(platforms, Platform{
                        Name:  platformName,
                        URL:   url,
                        Found: true,
                    })
                }
            }
        }
    }
    
    return platforms
}

func runGosearch(ctx context.Context, username string) (ExecResult, error) {
    path, err := gosearchPath()
    if err != nil {
        return ExecResult{}, fmt.Errorf("failed to locate gosearch binary: %w", err)
    }

    ctx, cancel := context.WithTimeout(ctx, 60*time.Second)
    defer cancel()

    cmd := exec.CommandContext(ctx, path, "-u", username)
    out, err := cmd.Output()
    exitCode := 0
    stderrStr := ""
    if err != nil {
        if ee, ok := err.(*exec.ExitError); ok {
            stderrStr = string(ee.Stderr)
            exitCode = ee.ExitCode()
        } else {
            return ExecResult{}, err
        }
    }

    outputStr := string(out)
    platforms := parseGosearchOutput(outputStr)

    return ExecResult{
        Username:  username,
        ExitCode:  exitCode,
        Platforms: platforms,
        RawOutput: outputStr,
        Stderr:    stderrStr,
    }, nil
}

func main() {
    // Install gosearch on startup; ignore errors only after retry
    ctx := context.Background()

    log.Println("Installing gosearch (this may take a moment)...")
    if err := installGosearch(ctx); err != nil {
        log.Printf("initial install failed: %v; will retry in 5s and continue startup", err)
        time.Sleep(5 * time.Second)
        if err2 := installGosearch(ctx); err2 != nil {
            log.Printf("retry install failed: %v; continuing — calls may fail until binary is available", err2)
        }
    }

    http.HandleFunc("/search", func(w http.ResponseWriter, r *http.Request) {
        username := r.URL.Query().Get("username")
        if username == "" {
            http.Error(w, "username query param is required", http.StatusBadRequest)
            return
        }

        res, err := runGosearch(r.Context(), username)
        if err != nil {
            http.Error(w, fmt.Sprintf("failed to run gosearch: %v", err), http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(res)
    })

    port := os.Getenv("PORT")
    if port == "" {
        port = "8081"
    }

    addr := ":" + port
    log.Printf("gosearch proxy server listening on %s", addr)
    if err := http.ListenAndServe(addr, nil); err != nil {
        log.Fatalf("server failed: %v", err)
    }
}
