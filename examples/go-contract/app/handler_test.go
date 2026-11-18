package app

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandlerMapsServiceErrors(t *testing.T) {
	fake := &fakeStore{result: Account{ID: "123", Name: "Example"}}
	service, _ := NewAccountService(fake)
	handler := NewAccountHandler(service)
	cases := []struct {
		query string
		want  int
	}{{"", http.StatusBadRequest}, {"?id=123", http.StatusOK}}
	for _, tt := range cases {
		req := httptest.NewRequest(http.MethodGet, "/accounts"+tt.query, nil)
		recorder := httptest.NewRecorder()
		handler.ServeHTTP(recorder, req)
		if recorder.Code != tt.want {
			t.Fatalf("query=%s got=%d want=%d", tt.query, recorder.Code, tt.want)
		}
	}
}
