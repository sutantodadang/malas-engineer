package main

import (
	"context"
	"errors"
	"example.com/malas-engineer/go-contract/app"
	"log"
	"net/http"
)

// Demo adapter; replace with sqlc *Queries in production. This file is the composition root.
type memoryStore struct{ items map[string]app.Account }

func (m *memoryStore) GetAccount(_ context.Context, id string) (app.Account, error) {
	a, ok := m.items[id]
	if !ok {
		return app.Account{}, app.ErrNotFound
	}
	return a, nil
}
func main() {
	store := &memoryStore{items: map[string]app.Account{"123": {ID: "123", Name: "Example"}}}
	service, err := app.NewAccountService(store)
	if err != nil {
		log.Fatal(err)
	}
	handler := app.NewAccountHandler(service)
	mux := http.NewServeMux()
	mux.Handle("/accounts", handler)
	err = http.ListenAndServe(":8080", mux)
	if err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
