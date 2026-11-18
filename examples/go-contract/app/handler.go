package app

import (
	"encoding/json"
	"errors"
	"net/http"
)

type AccountHandler struct{ service *AccountService }

func NewAccountHandler(service *AccountService) *AccountHandler {
	return &AccountHandler{service: service}
}

func (h *AccountHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	account, err := h.service.GetAccount(r.Context(), r.URL.Query().Get("id"))
	switch {
	case errors.Is(err, ErrInvalidID):
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	case errors.Is(err, ErrNotFound):
		http.Error(w, "not found", http.StatusNotFound)
		return
	case err != nil:
		http.Error(w, "internal error", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(account)
}
