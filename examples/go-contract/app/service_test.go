package app

import (
	"context"
	"errors"
	"testing"
)

type fakeStore struct {
	calls  int
	result Account
	err    error
}

func (f *fakeStore) GetAccount(_ context.Context, _ string) (Account, error) {
	f.calls++
	return f.result, f.err
}

func TestServiceUsesInjectedStore(t *testing.T) {
	fake := &fakeStore{result: Account{ID: "123", Name: "Example"}}
	service, err := NewAccountService(fake)
	if err != nil {
		t.Fatal(err)
	}
	got, err := service.GetAccount(context.Background(), "123")
	if err != nil || got.Name != "Example" || fake.calls != 1 {
		t.Fatalf("DI not used: result=%+v err=%v calls=%d", got, err, fake.calls)
	}
}
func TestInvalidIDSkipsStore(t *testing.T) {
	fake := &fakeStore{}
	service, _ := NewAccountService(fake)
	_, err := service.GetAccount(context.Background(), " ")
	if !errors.Is(err, ErrInvalidID) || fake.calls != 0 {
		t.Fatalf("invalid ID path violated: %v, calls=%d", err, fake.calls)
	}
}
func TestNilStoreRejected(t *testing.T) {
	if _, err := NewAccountService(nil); err == nil {
		t.Fatal("nil dependency accepted")
	}
}
