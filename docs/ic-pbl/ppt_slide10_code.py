# ── process_cash_payment (kiosk_controller.py:215-238) ───────────────────────

def process_cash_payment(self) -> tuple[list, int, dict]:
    snapshot = list(self.cart.items)
    final_amount = self.get_final_amount()
    change_result = self._active_payment.process()
    self._save_after_payment()
    self.cart.items = []
    self._active_payment = None
    self.log("현금 결제 완료")
    return snapshot, final_amount, change_result


# ── save_change_reserve (data_manager.py:134-138) ────────────────────────────

def save_change_reserve(self, data: dict) -> None:
    self._save("change_reserve.json", data)


# ── _save (data_manager.py:63-70) ────────────────────────────────────────────

def _save(self, filename: str, data) -> None:
    os.makedirs(self.data_dir, exist_ok=True)
    with open(self._path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
