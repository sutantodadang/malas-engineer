class RefreshService {
  constructor(store) {
    this.store = store;
  }

  async refresh(key, view = "summary") {
    return this.store.load(key, view);
  }
}

module.exports = { RefreshService };
