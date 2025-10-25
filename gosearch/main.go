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

type ExecResult struct {
    Username string `json:"username"`
    ExitCode int    `json:"exit_code"`
    Stdout   string `json:"stdout"`
    Stderr   string `json:"stderr"`
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

    return ExecResult{
        Username: username,
        ExitCode: exitCode,
        Stdout:   string(out),
        Stderr:   stderrStr,
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
