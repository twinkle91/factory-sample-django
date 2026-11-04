// Command notifier is a placeholder service that will send task reminders.
// It exists so the repository scan reports a Go project in this monorepo.
package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func health(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
	http.HandleFunc("/health", health)
	log.Println("notifier listening on :8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
