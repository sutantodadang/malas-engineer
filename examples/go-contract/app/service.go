package app

import (
	"context"
	"errors"
	"strings"
)

var ErrInvalidID = errors.New("account ID is required")
var ErrNotFound = errors.New("account not found")

// AccountStore is defined by its consumer. A sqlc *Queries can satisfy it directly.
type AccountStore interface {
	GetAccount(ctx context.Context, id string) (Account, error)
}

type Account struct {
	ID   string
	Name string
}

type AccountService struct{ store AccountStore }

func NewAccountService(store AccountStore) (*AccountService, error) {
	if store == nil {
		return nil, errors.New("account store is required")
	}
	return &AccountService{store: store}, nil
}

func (s *AccountService) GetAccount(ctx context.Context, id string) (Account, error) {
	if strings.TrimSpace(id) == "" {
		return Account{}, ErrInvalidID
	}
	return s.store.GetAccount(ctx, id)
}
